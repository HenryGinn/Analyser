from whatsapp import WhatsApp

path = "/home/henry/Downloads/WhatsApp Chats"

whatsapp = WhatsApp(path)
#whatsapp.update_folder_names()
whatsapp.initialise_chats()
whatsapp.process("preprocess")
