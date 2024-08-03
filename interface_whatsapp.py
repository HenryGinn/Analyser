from Services.whatsapp import WhatsApp

#path = "/home/henry/Downloads/WhatsApp Chats"
path = "/home/henry/Documents/Stuff/Data From Services/WhatsApp"

whatsapp = WhatsApp(path)
whatsapp.initialise_chats()
whatsapp.process("preprocess", force=True)
#whatsapp.process("read")
#self = whatsapp.chat_objects["Connections"]
#whatsapp.process("people")
