from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model.ui import StandardCard
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_model.ui import Image
import data
import reddit_api
import constant

sb = SkillBuilder()

session_posts = {}
session_index = {}


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):

        # build VUI
        speech_text = data.WELCOME_PROMPT

        # build GUI
        image = Image(data.UTIL_DATA["welcome_image"])
        card = StandardCard(data.SKILL_NAME, "", image)

        # build response
        handler_input.response_builder\
            .speak(speech_text)\
            .set_card(card).set_should_end_session(False)
        return handler_input.response_builder.response


class HelloWorldIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = data.WELCOME
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


def get_slot_value(intent):
    try:
        slots = intent.slots
        slot_sub_reddit = slots["subreddit"]
        if not slot_sub_reddit.resolutions:
            return ""
        resolution = slot_sub_reddit.resolutions[0]
        if resolution.status.code == "ER_SUCCESS_MATCH":
            return slot_sub_reddit.values[0].value.name
        elif resolution.status.code == "ER_SUCCESS_NO_MATCH":
            return slot_sub_reddit.value
    except Exception:
        pass
    return "news"


class ReadIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ReadIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        intent = handler_input.request_envelope.request.intent
        sub_reddit_name = get_slot_value(intent)
        if sub_reddit_name:
            hot_trending_posts_titles = reddit_api.get_subreddit_posts_by_name(sub_reddit_name)
        else:
            hot_trending_posts_titles = reddit_api.get_hot_trending_post_titles("popular",
                                                                                 constant.HOT_TRENDING_POSTS_COUNT)
        session_id = handler_input.request_envelope.session.session_id
        if not hot_trending_posts_titles:
            speech_text = data.SORRY_EMPTY_PROMPT
        else:
            speech_text = hot_trending_posts_titles[0]
            session_posts[session_id] = hot_trending_posts_titles
            session_index[session_id] = 0

        handler_input.response_builder.speak(speech_text).set_card(SimpleCard(speech_text, speech_text))\
                .set_should_end_session(False)

        return handler_input.response_builder.response


class NextIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ReadIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        hot_trending_posts_titles = reddit_api.get_hot_trending_posts_titles("popular",
                                                                             constant.HOT_TRENDING_POSTS_COUNT)
        for post_title in hot_trending_posts_titles:
            handler_input.response_builder.speak(post_title).set_card(SimpleCard(post_title, post_title))

        return handler_input.response_builder.response


class UpvoteIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("UpvoteIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "upvote intent"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("upvote intent", speech_text))
        return handler_input.response_builder.response


class AddCommentIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("Intent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Hello World"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class WriteCommentIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Hello World"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say hello to me!"
        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = data.GOODBYE_PROMPT
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # any cleanup logic goes here
        return handler_input.response_builder.response


class AllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # Log the exception in CloudWatch Logs
        print(exception)
        speech = "Sorry, I didn't get it. Can you please say it again!!"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


''' Add all request handlers here '''
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ReadIntentHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(AllExceptionHandler())
handler = sb.lambda_handler()
