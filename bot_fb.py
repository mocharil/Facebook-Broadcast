from telegram.ext import CommandHandler,Filters, Updater, MessageHandler

import os
import json,re
print('================BOT READY=================')
print('ketik: /post untuk mengganti pesan yang akan di posting')
print('ketik: /help untuk bantuan')

def make_dir(path):
    try:
        os.mkdir(path)
    except:
        pass
path = os.getcwd()
        
def posting(bot, update):
    text=update.message.text.split(None,1)[-1]
    d=text.replace('<username>','||||').replace('<pesan>','||||').replace('<waktu>','||||').replace('<jenis>','||||').split('||||')
    if len(d)==5:
        name=d[1].replace(' ','')
        message=d[2]
        jenis=d[3].replace(' ','')
        time=d[4].replace(' ','')
    else:
        name=d[0].replace(' ','')
        message=d[1]
        jenis=d[2].replace(' ','')
        time=d[3].replace(' ','')
    
    print('\n==============================================')
    print('username: '+name)
    print('\n==============================================')
    print('pesan: '+message)
    print('\n==============================================')
    print('jenis postingan: '+jenis)
    print('\n==============================================')
    print('waktu kirim: '+time)
    
    if 'group' in jenis or 'gruop' in jenis:
        jenis='grup'
        
    path1=path+'/{}/'.format(name)
    make_dir(path1)
    make_dir(path1+'photo_personal')
    make_dir(path1+'photo_grup')

    with open(path1+'posting_{}_{}.json'.format(name,jenis),'w') as f:
        json.dump({'message':message,'time':time,'username':name,'jenis':jenis},f)
        
    try:
        os.remove(path1+'runner_{}.txt'.format(jenis))
    except:
        pass  
     
    
    update.message.reply_text('postingan telah terupdate menjadi :\nnama pengirim : {}'.format(name))
    update.message.reply_text('\npesan: {}'.format(message)) 
    update.message.reply_text('\nwaktu kirim: tiap {} menit'.format(time))
    update.message.reply_text('\ndiposting ke : {}'.format(jenis))
    

def status(bot, update):
    print('\n=======================status saat ini===========================')
    for name in os.listdir():
        try:
            for i in os.listdir(path+'/'+name):
                if '.json' in i:
                    with open(path+'/'+name+'/'+i) as f:
                        data=json.load(f) 
                    update.message.reply_text('Pesan yang dikirim:\n{}'.format(data))
        except:
            pass
 
        
    
    
def help(bot, update):
    print('\n=======================help===========================')
    print('format :\n/post <username> username facebook anda <pesan> pesan anda <jenis> dikirim personal atau ke grup <waktu> tiap berapa menit dikirim')
    print('contoh :\n/post <username> telkom21 <pesan> selamat anda mendapat hadiah <jenis> personal <waktu> 50')
    print('jika anda ingin mengupload foto, masukan foto ke folder photo_personal atau di photo_grup')
    
    update.message.reply_text('format :\n/post <username> username facebook anda <pesan> pesan anda <jenis> dikirim personal atau ke grup <waktu> tiap berapa menit dikirim')  
    update.message.reply_text('contoh :\n/post <username> telkom21 <pesan> selamat anda mendapat hadiah <jenis> personal <waktu> 50')
    update.message.reply_text('jika anda ingin mengupload foto, masukan foto ke folder photo_personal atau di photo_grup')

def main(TOKEN):
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('post',posting,filters=Filters.private))

    dp.add_handler(CommandHandler('help',help,filters=Filters.private))
    
    dp.add_handler(CommandHandler('status',status,filters=Filters.private))

    updater.start_polling()

    updater.idle()



if __name__ == '__main__':
    token='Your TOKEN telegram bot'
        
    main(token)
