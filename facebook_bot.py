#pip install git+https://www.github.com/mobolic/facebook-sdk
import facebook 
import json
import schedule
import time
import os
import datetime

def send_photos(path, send_to, message):
    date_now=datetime.datetime.now()
    if int(str(date_now)[10:13])>=8:
        print('sending photos to '+send_to)
        imgs_id = []
        for img in os.listdir(path):
            photo = open(path+img, "rb")
            imgs_id.append(graph.put_photo(photo, album_id=path,published=False)['id'])
            photo.close()

        args=dict()
        args["message"]=message
        for img_id in imgs_id:
            key="attached_media["+str(imgs_id.index(img_id))+"]"
            args[key]="{'media_fbid': '"+img_id+"'}"
        if send_to=='me':
            graph.request('me/feed', args=None, post_args=args, method='POST')
            print('Anda telah update status dengan foto')
        else:
            for s in daftar_group:
                try:
                    l = s.values()    
                    object_id=tuple(l)[3]
                    graph.request('{}/feed'.format(object_id), args=None, post_args=args, method='POST')
                    print('Pesan telah di posting ke group %s'%tuple(l)[0].encode('utf-8',errors='ignore')+' dengan photo')
                    time.sleep(3)
                except:
                    pass



def login(status=True):
    print('\n====================LOGIN====================')
    name=input('username: ')
    if status==True:
        try:
            access_token=open('facebook_{}.txt'.format(name)).read()
            print('\n============ WELCOME BACK {} ================='.format(name.upper()))
        except:
            with open('facebook_{}.txt'.format(name), 'w') as f:
                access_token=input('access_token: ')
                f.write(access_token)
          
    else:
        try:
            access_token=open('facebook_{}.txt'.format(name)).read()
            print('\n============ WELCOME BACK {} ================='.format(name.upper()))
        except:
            with open('facebook_{}.txt'.format(name), 'w') as f:
                access_token=input('access_token: ')
                f.write(access_token)
    return access_token,name
    
x=True
token,name=login()

while x:
    try:
        graph=facebook.GraphAPI(token, version='3.1')
        groups = graph.get_connections(id='me', connection_name='groups')
        x=False
    except:
        print('\n>>>>>>>>>>>>>>>>>>>>>> ACCESS TOKEN ANDA SALAH COBA LAGI <<<<<<<<<<<<<<<<<')
        os.remove('facebook_{}.txt'.format(name))
        token,name=login(status=False)

print('\n=============LOGIN SUCCESS============')

daftar_group = groups['data']

def make_dir(path):
    try:
        os.mkdir(path)
    except:
        pass

path_inti=os.getcwd()
make_dir(path_inti+'\\'+name)

path_name=path_inti+'\\'+name

message = '' 

with open(path_name+'\\posting_{}_personal.json'.format(name),'w') as f:
    json.dump({'message':message,'time':'60','username':name,'jenis':'personal'},f)

with open(path_name+'\\posting_{}_grup.json'.format(name),'w') as f:
    json.dump({'message':message,'time':'60','username':name,'jenis':'grup'},f)
    

def post_to_group():
    date_now=datetime.datetime.now()
    if int(str(date_now)[10:13])>=8:
        with open(path_name+'\\posting_{}_grup.json'.format(name)) as f:
            data=json.load(f)
        message=data['message']
        time.sleep(10)
        if len(os.listdir(path_name+'\\photo_grup'))==0:
            if message =='':
                print('update pesan anda di akun bot telegram @set_facebook_bot')
            else:
                for s in daftar_group:
                    l = s.values()    
                    object_id=tuple(l)[3]
                    try:
                        try:
                            graph.put_object(object_id, 'feed',message=message)
                            print('Pesan telah di posting ke group %s'%tuple(l)[0].encode('utf-8',errors='ignore'))
                            time.sleep(2)
                        except:
                            pass
                    except Exception as e:
                        print(e)
                        try:
                            message=message+'.'
                            graph.put_object(object_id, 'feed',message=message)
                            print('Pesan telah di posting ke group %s'%tuple(l)[0].encode('utf-8',errors='ignore'))
                            with open(path_name+'\\posting_{}_grup.json'.format(name),'w') as f:
                                json.dump({'message':message, 'time':data['time']},f)
                            time.sleep(3)
                        except Exception as e1:
                            print(e1)
                   
        else:
            try:
                send_photos(path_name+'\\photo_grup\\','grup', message)
            except:
                pass
        
def post_to_wall():
    date_now=datetime.datetime.now()
    if int(str(date_now)[10:13])>=8:
        with open(path_name+'\\posting_{}_personal.json'.format(name)) as f:
            data=json.load(f)
        message=data['message']
        if message =='':
            print('update pesan anda di akun bot telegram @set_facebook_bot')
        else:
            if len(os.listdir(path_name+'\\photo_personal'))==0:
                try:
                    graph.put_object("me", "feed", message=message)
                    print('Anda telah update status')
                except:
                    message=message+'.'
                    graph.put_object("me", "feed", message=message)
                    print('Anda telah update status')
                    with open(path_name+'\\posting_{}_personal.json'.format(name),'w') as f:
                        json.dump({'message':message,'time':data['time']},f)
            else:
                try:
                    send_photos(path_name+'\\photo_personal\\','me', message)
                except:
                    pass

def error_personal():
    open(path_name+'\\runner_personal.txt').read()
def error_grup():
    open(path_name+'\\runner_grup.txt').read()
    
print('\n=============STATUS============') 
print('update pesan anda di akun bot telegram @set_facebook_bot')
    
p=False
while True:    
    with open(path_name+'\\posting_{}_grup.json'.format(name)) as f:
        time_grup=json.load(f)['time']
    with open(path_name+'\\posting_{}_personal.json'.format(name)) as f:
        time_personal=json.load(f)['time']
        
    with open(path_name+'\\runner_grup.txt', 'w') as f:
        f.write('Yes')

    with open(path_name+'\\runner_personal.txt', 'w') as f:
        f.write('Yes')
        
    schedule.clear()
    schedule.every(int(time_personal)).minutes.do(post_to_wall)
    schedule.every(int(time_grup)).minutes.do(post_to_group)
    schedule.every(1).seconds.do(error_personal)
    schedule.every(1).seconds.do(error_grup)
    while True:
        try:
            schedule.run_pending()
        except KeyboardInterrupt:
            p = True
            break
        except FileNotFoundError:
            break
            
    if p==True:
        break
        
print('>>>>>>>>>>>>>>>>>>>>>>>disconected<<<<<<<<<<<<<<<<<<<<<<<\n')