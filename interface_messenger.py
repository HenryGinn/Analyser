from whatsapp import WhatsApp

path = "/home/henry/Downloads/WhatsApp Chats"

whatsapp = WhatsApp(path)
whatsapp.initialise_chats()
#whatsapp.process("preprocess", force=True)
whatsapp.process("read")
self = whatsapp.chat_objects["Connections"]
whatsapp.process("people")
