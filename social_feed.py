from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.interfaces.display import (RenderTemplateDirective, BodyTemplate6, BodyTemplate2)
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.response_helper import (get_plain_text_content)
import data
from data import Post
import reddit_api
import constant
import sys
import os

sb = SkillBuilder()

session_posts = {}
session_index = {}


def get_next_item(session_id):
    if not session_id:
        return data.SORRY_EMPTY_PROMPT
    posts = session_posts.get(session_id, [])
    index = session_index.get(session_id, -1)
    if not posts or index == -1:
        return data.SORRY_EMPTY_PROMPT
    index += 1
    if index < len(posts):
        speech_text = posts[index].title
        session_index[session_id] = index
    else:
        try:
            session_posts.pop(session_id)
            session_index.pop(session_id)
        except Exception as e:
            reddit_api.print_exception_details(e)
        speech_text = data.SORRY_EMPTY_PROMPT
    return speech_text


def get_current_item(session_id):
    if not session_id:
        return data.SORRY_EMPTY_PROMPT
    posts = session_posts.get(session_id, [])
    index = session_index.get(session_id, -1)
    if not posts or index == -1:
        return data.SORRY_EMPTY_PROMPT
    if index < len(posts):
        speech_text = posts[index].title
        session_index[session_id] = index
    else:
        try:
            session_posts.pop(session_id)
            session_index.pop(session_id)
        except Exception as e:
            reddit_api.print_exception_details(e)
        speech_text = data.SORRY_EMPTY_PROMPT
    return speech_text


def get_current_post(session_id):
    current_post = Post()
    if not session_id:
        return current_post
    posts = session_posts.get(session_id, [])
    index = session_index.get(session_id, -1)
    if not posts or index == -1:
        return current_post
    if index < len(posts):
        current_post = posts[index]
        session_index[session_id] = index
    else:
        try:
            session_posts.pop(session_id)
            session_index.pop(session_id)
        except Exception as e:
            reddit_api.print_exception_details(e)

    return current_post


def clear_item(session_id):
    if not session_id:
        return
    posts = session_posts.get(session_id, [])
    index = session_index.get(session_id, -1)
    if not posts or index == -1:
        return
    try:
        session_posts.pop(session_id)
        session_index.pop(session_id)
    except Exception as e:
        reddit_api.print_exception_details(e)


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # build VUI
        speech_text = data.WELCOME_PROMPT

        # build GUI
        template = BodyTemplate6(
            background_image=data.welcome_image,
            text_content=get_plain_text_content(primary_text="Welcome to " + data.SKILL_NAME))

        print("LaunchRequest template: " + template.to_str())

        # build response
        handler_input.response_builder \
            .speak(speech_text) \
            .add_directive(RenderTemplateDirective(template)) \
            .set_should_end_session(False)
        return handler_input.response_builder.response


def print_exception_details():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)


def get_slot_value(intent):
    try:
        slots = intent.slots
        slot_sub_reddit = slots["subreddit"]
        print("Getting slot value")
        slot_sub_reddit = slot_sub_reddit.to_dict()
        print("slot_sub_reddit: ", slot_sub_reddit)

        if not slot_sub_reddit["resolutions"]:
            print("NO Resolution")
            return constant.DEFAULT_SUB_REDDIT
        resolution = slot_sub_reddit["resolutions"]["resolutions_per_authority"][0]
        print("resolution: ", resolution)

        if resolution["status"]["code"] == "ER_SUCCESS_MATCH":
            print("Slot MATCH")
            return resolution["values"][0]["value"]["name"]
        elif resolution["status"]["code"] == "ER_SUCCESS_NO_MATCH":
            print("NO SLOT MATCH")
            return slot_sub_reddit["value"]
    except Exception as e:
        reddit_api.print_exception_details(e)

    return constant.DEFAULT_SUB_REDDIT


class ReadIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ReadIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        intent = handler_input.request_envelope.request.intent
        sub_reddit_name = get_slot_value(intent)
        print("Resolving sub reddit name to ", sub_reddit_name)
        hot_trending_posts_posts = reddit_api.get_subreddit_posts_by_name(sub_reddit_name)
        speech_text = data.SORRY_EMPTY_PROMPT
        try:
            session_id = handler_input.request_envelope.session.session_id
            print("session_id here is", session_id)

            for i in range(len(hot_trending_posts_posts)):
                if hot_trending_posts_posts[i].title:
                    speech_text = hot_trending_posts_posts[i].title
                    session_index[session_id] = i
                    session_posts[session_id] = hot_trending_posts_posts
                    break
        except Exception as e:
            reddit_api.print_exception_details(e)

        print("SpeechText ", speech_text)

        # Build GUI
        session_id = handler_input.request_envelope.session.session_id
        current_post = get_current_post(session_id)
        template = get_gui_template(current_post)

        # Build response
        handler_input.response_builder \
            .speak(speech_text) \
            .add_directive(RenderTemplateDirective(template))\
            .set_should_end_session(False)

        return handler_input.response_builder.response


class NextIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.NextIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        session_id = handler_input.request_envelope.session.session_id
        speech_text = get_next_item(session_id)

        # Build GUI
        current_post = get_current_post(session_id)
        template = get_gui_template(current_post)

        # Build response
        handler_input.response_builder \
            .speak(speech_text) \
            .add_directive(RenderTemplateDirective(template)) \
            .set_should_end_session(False)

        return handler_input.response_builder.response


class RepeatIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # Build VUI
        session_id = handler_input.request_envelope.session.session_id
        current_post = get_current_post(session_id)
        current_post_title = current_post.title
        if current_post is None:
            speech_text = data.SORRY_EMPTY_PROMPT
        else:
            speech_text = current_post_title

        # Build GUI
        template = get_gui_template(current_post)

        # Build response
        handler_input.response_builder\
            .speak(speech_text)\
            .add_directive(RenderTemplateDirective(template))

        return handler_input.response_builder.response


def get_gui_template(current_post):
    current_post_title = current_post.title
    current_post_text = current_post.text
    current_post_author = current_post.author
    current_post_subreddit = "r/" + current_post.sub_reddit_name + "     Posted by u/" + current_post_author
    current_post_url = current_post.url
    template = BodyTemplate2(
        background_image=data.default_background,
        title=current_post_subreddit,
        text_content=get_plain_text_content(primary_text=current_post_title,
                                            secondary_text=current_post_text,
                                            tertiary_text="\n ⬆️ " + str(current_post.up_votes) + " ⬇️"),
        image=data.get_image_by_url(current_post_url))
    print("Generated GUI template: " + template.to_str())
    return template


class UpvoteIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("UpvoteIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        session_id = handler_input.request_envelope.session.session_id
        current_post_id = get_current_post(session_id).id
        if not current_post_id:
            speech_text = data.UNABLE_TO_UPVOTE_PROMPT
        elif reddit_api.upvote_a_post(current_post_id):
            speech_text = data.UPVOTE_SUCCESSFUL_PROMPT
        else:
            speech_text = data.UNABLE_TO_UPVOTE_PROMPT

        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Try ask, what's trending"
        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or \
               is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = data.GOODBYE_PROMPT
        session_id = handler_input.request_envelope.session.session_id
        clear_item(session_id)
        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # any cleanup logic goes here
        clear_item(handler_input.request_envelope.session.session_id)
        return handler_input.response_builder.response


class AllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response

        # Log the exception in CloudWatch Logs
        tb = sys.exc_info()[2]
        print(exception.with_traceback(tb))
        
        speech = "Sorry, I didn't get it. Can you please say it again?"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


''' Add all request handlers here '''
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ReadIntentHandler())
sb.add_request_handler(NextIntentHandler())
sb.add_request_handler(UpvoteIntentHandler())
sb.add_request_handler(RepeatIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_exception_handler(AllExceptionHandler())
sb.add_request_handler(SessionEndedRequestHandler())
handler = sb.lambda_handler()
