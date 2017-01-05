from twilio.rest import TwilioRestClient as TRC


def twilio_client():
    account_sid   = "AC79432a906b5df034fa4604d80dee6079"
    auth_token    = "077422f1a2129d43670ca8b802cef484"
    return TRC(account_sid, auth_token)

client = twilio_client()
twilio_number = "+18133363411"


body = "Drake just dropped a new song called Back to Back, check it out here soundcloud://tracks/216846955"
client.messages.create(to = "+18139095372", from_ = twilio_number, body = body)
