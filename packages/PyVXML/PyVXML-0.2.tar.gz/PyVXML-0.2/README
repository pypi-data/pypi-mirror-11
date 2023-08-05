PyVXML Project
=======================

Sample Uses:
-----------

from PyVXML import PyVXML

vxml = PyVXML(version='2.0')
vxml.start_form(fid='subscriptionmsg')
vxml.start_block()
vxml.start_prompt(bargein='true')
vxml.start_audio(src='http://example.com/prompts/voicechat/mainmenu/Thanks.wav')
vxml.end_audio()
vxml.end_prompt()
vxml.start_disconnect()
vxml.end_block()
vxml.end_form()

vxml_xml = vxml.generate()
