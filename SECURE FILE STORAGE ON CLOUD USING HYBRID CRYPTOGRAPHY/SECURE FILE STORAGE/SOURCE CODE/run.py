import binascii
from flask import Flask, render_template, request,session,send_from_directory,Response
import os
import random
import pymysql
from pymsgbox import *
import string
from Rest import Rest
from MyAES import MyAES
from MyBlowFish import MyBlowFish
from MyTrippleDesk import MyTrippleDesk
from Mail import send_email

app=Flask(__name__)
app.secret_key = 'dfghjjhgfdfghjuytresdcvb'
conn=pymysql.connect(host="localhost",user="root",password="maheshg@6714",db="hybrid")
cursor=conn.cursor()
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
  return render_template('adminlog.html')

@app.route('/cloud')
def cloud():
  return render_template('cloudLogin.html')

@app.route('/adminlog1')
def adminlog1():
    username = request.args.get('username')
    password = request.args.get('password')
    if username == 'admin' and  password=='admin':
        return render_template('adminhome.html')
    else:
        alert(text='INVALID LOGIN DETAILS', title='LOGIN STATUS', button='OK')
        return render_template('adminlog.html')

@app.route('/adminhome')
def adminhome():
    return render_template('adminhome.html')

@app.route('/adminlogout')
def adminlogout():
    return render_template("index.html")

@app.route('/cloudLogin1')
def cloudLogin1():
    username = request.args.get('username')
    password = request.args.get('password')
    if username == 'cloud' and  password=='cloud':
        return render_template('cloudHome.html')
    else:
        alert(text='INVALID LOGIN DETAILS', title='LOGIN STATUS', button='OK')
        return render_template('cloudLogin.html')

@app.route('/oregister')
def register():
    return render_template("oregister.html")

@app.route('/oregister1',methods=['POST'])
def oregister1():
    target = os.path.join(APP_ROOT, 'images/')
    for upload in request.files.getlist("file"):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        phone = request.form.get('phone')
        filename = upload.filename
        print(filename)
        destination = "/".join([target, filename])
        upload.save(destination)
        resultvalue = cursor.execute("select * from oregistration where username='"+username+"' or email='"+email+"'")
        conn.commit()

        userDetails = cursor.fetchall()
        if resultvalue > 0:
            alert(text='User Already exist', title='Registration STATUS', button='OK')
            return render_template('register.html')

        else:

                result = cursor.execute(
                    " insert into oregistration(name,username,email,password,phone,pic)values('" + name + "','" + username + "','" + email + "','" + password + "','" + phone + "','"+upload.filename+"')");
                conn.commit()
                alert(text='Registration success', title='Registration STATUS', button='OK')

                return render_template('ologin.html')

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

@app.route('/ologin')
def login():
    return render_template('ologin.html')

@app.route('/ologin1')
def ologin1():
    username = request.args.get('username')
    password = request.args.get('password')
    result = cursor.execute(" select * from oregistration where username='" + username + "' and password='" + password + "' and   status='authorize'")
    details=cursor.fetchall()
    conn.commit()
    if result > 0:
        for user in details:
                 session['username'] = user[2]
                 session['owner_id']=user[0]
                 session['email']=user[3]
        return render_template('ownerHome.html')




    else:
        alert(text='Invalid Login Details', title='Login STATUS', button='OK')

        return render_template('ologin.html')

@app.route('/uregister')
def uregister():
    return render_template("uregister.html")


@app.route('/uregister1',methods=['POST'])
def uregister1():
    target = os.path.join(APP_ROOT, 'images/')
    for upload in request.files.getlist("file"):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        phone = request.form.get('phone')
        filename = upload.filename
        print(filename)
        destination = "/".join([target, filename])
        upload.save(destination)
        resultvalue = cursor.execute("select * from uregistration where username='"+username+"' and email='"+email+"'")
        conn.commit()
        userDetails = cursor.fetchall()
        if resultvalue > 0:
            alert(text='User Already exist', title='Registration STATUS', button='OK')
            return render_template('uregister.html')
        else:
                result = cursor.execute(
                    " insert into uregistration(name,username,email,password,phone,pic)values('" + name + "','" + username + "','" + email + "','" + password + "','" + phone + "','"+upload.filename+"')");
                conn.commit()
                alert(text='Registration success', title='Registration STATUS', button='OK')
                return render_template('ulogin.html')

@app.route('/ulogin')
def ulogin():
    return render_template('ulogin.html')

@app.route('/ulogin1')
def ulogin1():
    username = request.args.get('username')
    password = request.args.get('password')
    result = cursor.execute(" select * from uregistration where username='" + username + "' and password='" + password + "' and   status='authorize'")
    details=cursor.fetchall()
    conn.commit()
    if result > 0:
        for user in details:
                 session['username'] = user[2]
                 session['user_id']=user[0]
                 session['email']=user[3]
        return render_template('userHome.html')




    else:
        alert(text='Invalid Login Details', title='Login STATUS', button='OK')
        return render_template('ulogin.html')

@app.route('/verifyUser')
def verifyUser():
    image_names = os.listdir('./images')
    resultvalue = cursor.execute("select * from uregistration")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('allusers.html', userDetails=userDetails)
    else:
        alert(text='Users details are not available', title='Details STATUS', button='OK')
        return render_template('adminhome.html')

@app.route('/activateuser')
def activateuser():
        req_id=request.args.get('Id')
        query=cursor.execute("select * from uregistration where o_id='"+req_id+"'")
        conn.commit()
        querydetails=cursor.fetchall()
        for user in querydetails:
            email=user[3]
            #SMTP.EmailSending.send_email("","Activation Response","Your Registration Request Activated from the cloud server",email)
            send_email("Activation Response", "Your Registration Request Activated from the Administrator", email)

            resultvalue = cursor.execute("update uregistration set status='authorize' where  o_id='"+req_id+"' ")
            conn.commit()
            if resultvalue > 0:
                return verifyUser()
            else:
                alert(text='User Activating Fails', title='Activation STATUS', button='OK')
                return verifyUser()

@app.route('/deactivateuser')
def deactivateuser():
        req_id=request.args.get('Id')
        query=cursor.execute("select * from uregistration where o_id='"+req_id+"'")
        conn.commit()
        querydetails=cursor.fetchall()
        for user in querydetails:
            email=user[3]
            #SMTP.EmailSending.send_email("","Activation Response","Your Registration Request DeActivated from the cloud server",email)
            send_email("Activation Response", "Your Registration Request DeActivated from the Administrator", email)
            resultvalue = cursor.execute("update uregistration set status='unauthorized' where  o_id='"+req_id+"' ")
            conn.commit()
            if resultvalue > 0:
                return verifyUser()
            else:
                alert(text='User Activating Fails', title='Activation STATUS', button='OK')
                return verifyUser()

@app.route('/verifyOwner')
def verifyOwner():
    image_names = os.listdir('./images')
    resultvalue = cursor.execute("select * from oregistration")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('allowners.html', userDetails=userDetails)
    else:
        alert(text='Users details are not available', title='Details STATUS', button='OK')
        return render_template('adminhome.html')

@app.route('/activateowner')
def activateowner():
        req_id=request.args.get('Id')
        query=cursor.execute("select * from oregistration where o_id='"+req_id+"'")
        conn.commit()
        querydetails=cursor.fetchall()
        for user in querydetails:
            email=user[3]
            #SMTP.EmailSending.send_email("","Activation Response","Your Registration Request Activated from the cloud server",email)
            send_email("Activation Response", "Your Registration Request Activated from the Administrator", email)
            resultvalue = cursor.execute("update oregistration set status='authorize' where  o_id='"+req_id+"' ")
            conn.commit()
            if resultvalue > 0:
                return verifyOwner()
            else:
                alert(text='User Activating Fails', title='Activation STATUS', button='OK')
                return verifyOwner()

@app.route('/deactivateowner')
def deactivateowner():
        req_id=request.args.get('Id')
        query=cursor.execute("select * from oregistration where o_id='"+req_id+"'")
        conn.commit()
        querydetails=cursor.fetchall()
        for user in querydetails:
            email=user[3]
           # SMTP.EmailSending.send_email("","Activation Response","Your Registration Request DeActivated from the cloud server",email)
            send_email("Activation Response", "Your Registration Request DeActivated from the Administrator", email)
            resultvalue = cursor.execute("update oregistration set status='unauthorized' where  o_id='"+req_id+"' ")
            conn.commit()
            if resultvalue > 0:
                return verifyOwner()
            else:
                alert(text='User Activating Fails', title='Activation STATUS', button='OK')
                return verifyOwner()

@app.route('/uploadFile')
def upload():
        return render_template('uploadfile.html')


@app.route('/uploadfile1',methods=['POST'])
def uploadfile1():
    try:
        username = session['username']
        filename=request.form.get('fname')
        desc=request.form.get('dsc')
        file =request.files['myfile']
        newfiledate=file.read()
        data=str(newfiledate)
        # AES Implementation
        print(data[2:-1])
        data = data[2:-1]
        myaes = MyAES()
        aeskey, aesdataTuple = myaes.encrypt_AES_GCM(str.encode((data)))
        myiv = None
        mykey = None
        myEncrypted = None
        alName = None
        if(len(data)>100):
            print('trippledesk')
            alName = 'TrippleDesk'
            myTrippleDsk = MyTrippleDesk()
            myiv, mykey, myEncrypted =  myTrippleDsk.encrypt_trippleDesk(aesdataTuple[0])
        else:
            print('blowfish')
            alName = 'BlowFish'
            myBlowfish = MyBlowFish()
            myiv, mykey, myEncrypted  = myBlowfish.encrypt_blowFish(aesdataTuple[0])

        aeskey = binascii.hexlify(aeskey)
        aesdataTuple = (binascii.hexlify(aesdataTuple[0]),binascii.hexlify(aesdataTuple[1]),binascii.hexlify(aesdataTuple[2]))
        myiv = binascii.hexlify(myiv)
        mykey = binascii.hexlify(mykey)
        myEncrypted = binascii.hexlify(myEncrypted)
        aeskey = aeskey.decode(encoding='UTF-8')
        aesdataTuple = (aesdataTuple[0].decode(encoding='UTF-8'), aesdataTuple[1].decode(encoding='UTF-8'),aesdataTuple[2].decode(encoding='UTF-8'))
        myiv = myiv.decode(encoding='UTF-8')
        mykey = mykey.decode(encoding='UTF-8')
        myEncrypted = myEncrypted.decode(encoding='UTF-8')

        print(aeskey)
        print(aesdataTuple)
        print(myiv)
        print(mykey)
        print(myEncrypted)
        data1 = myEncrypted
        seglen = int(len(data1)/7)
        start = 0                   #0
        end = seglen-1              #9
        efragment1 = data1[:end]
        start = end             #10
        end = start + seglen - 1    #19
        efragment2 = data1[start:end]
        start = end            #20
        end = start + seglen - 1    #29
        efragment3 = data1[start:end]
        start = end
        end = start + seglen - 1
        efragment4 = data1[start:end]
        start = end
        end = start + seglen - 1
        efragment5 = data1[start:end]
        start = end
        end = start + seglen - 1
        efragment6 = data1[start:end]
        start = end
        end = -1
        efragment7 = data1[start:]
        print(len(data1))
        print(len(efragment1+efragment2+efragment3+efragment4+efragment5+efragment6+efragment7))
        rest = Rest()
        url = 'files/' + session['username'] +'/'+ filename;
        firebasedata = '{"fragment1":"' + efragment1 + '", "fragment2":"' + efragment2 + '", "fragment3":"' + efragment3 + '","fragment4":"' + efragment4 + '","fragment5":"' + efragment5 + '","fragment6":"' + efragment6 + '","fragment7":"' + efragment7 + '"}'
        rest.put(url=url, data=firebasedata)

        letters = string.ascii_lowercase
        keyy= ''.join(random.choice(letters) for i in range(10))
        result = cursor.execute(
            "insert into files(fname,username,descc,fdata,datee,etype,aeskey,aesctext,aesiv,authTag,myiv,mykey,myEncrypted,efrag1,efrag2,efrag3,efrag4,efrag5,efrag6,efrag7)values('" + filename + "','" + username + "','" + desc + "','" + data1 + "',now(),'" +alName+ "','"+str(aeskey)+"','"+str(aesdataTuple[0])+"','"+str(aesdataTuple[1])+"','"+str(aesdataTuple[2])+"','"+str(myiv)+"','"+str(mykey)+"','"+str(myEncrypted)+"','"+efragment1+"','"+efragment2+"','"+efragment3+"','"+efragment4+"','"+efragment5+"','"+efragment6+"','"+efragment7+"')");
        conn.commit()
        if result > 0:
            return upload1(cursor.lastrowid)
        else:
            alert(text='File Uploded Fails', title='File STATUS', button='OK')
            return upload()

    except Exception as e:
        print(e)
        alert(text='Duplicate File Name', title='File STATUS', button='OK')
        return upload()

@app.route('/upload1')
def upload1(fid):
    cursor.execute("select * from files where f_id='"+str(fid)+"'")
    fdel=cursor.fetchall()
    return render_template('upload1.html',fdel=fdel)


@app.route('/upload3')
def upload3():
    alert(text='File Uploded Success', title='File STATUS', button='OK')
    return upload()


@app.route('/viewuploadFile')
def viewuploadFile():
    username = session['username']
    resultvalue = cursor.execute("select * from files where username='"+username+"' ")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('viewfiles.html', userDetails=userDetails)
    else:
        alert(text='File Uploded Details are onot Available', title='File STATUS', button='OK')
        return render_template('ownerHome.html')

@app.route('/ownerlogout')
def ownerlogout():
    session.pop('username', None)
    session.pop('email', None)
    session.pop('owner_id', None)
    return render_template('index.html')

@app.route('/aviewuplodedfiles')
def aviewuplodedfiles():
    resultvalue = cursor.execute("select * from files")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('aviewfiles.html', userDetails=userDetails)
    else:
        alert(text='File Uploded Details are not Available', title='File STATUS', button='OK')
        return adminhome()

@app.route('/seadaccessrequest')
def seadaccessrequest():
    userId = session['user_id']
    username = session['username']
    a=cursor.execute("select * from accessrequest where searchbyid='"+str(userId)+"' and searchby='"+username+"'")
    b = cursor.execute(
        "select * from accessrequest where searchbyid='" + str(
            userId) + "' and searchby='" + username + "' and status='accept'")

    if a > 0:
        alert(text='You Already Sent Request Please wait for the response', title='Request STATUS', button='OK')
        return render_template('userHome.html')
    elif b > 0:
        alert(text='You Already Sent Request ', title='Request STATUS', button='OK')
        return render_template('userHome.html')


    else:
         return render_template('accessRequest.html')


@app.route('/accessrequest')
def accessrequest():
    userId = session['user_id']
    username = session['username']
    a=cursor.execute("insert into accessrequest(searchbyid,searchby,datee) values('"+str(userId)+"','"+username+"',now())")
    conn.commit()
    if a > 0 :
        alert(text='Request sent Success ', title='Request STATUS', button='OK')
        return seadaccessrequest()
    else:
        alert(text='Request sent Fails ', title='Request STATUS', button='OK')
        return seadaccessrequest()

@app.route('/useraccessreq')
def useraccessreq():
        resultvalue = cursor.execute("select * from accessrequest ")
        conn.commit()
        details=cursor.fetchall()

        if resultvalue > 0:
            return render_template('viewaccessrequest.html',reqdetails=details)
        else:
            alert(text='Request Details are not available ', title='Request STATUS', button='OK')
            return render_template('userHome.html')


@app.route('/verifyaccessrequest')
def verifyaccessrequest():
        req_id=request.args.get('Id')
        query=cursor.execute("select * from uregistration where o_id='"+req_id+"'")
        conn.commit()
        querydetails=cursor.fetchall()
        email=""
        for user in querydetails:
            email=user[3]
        resultvalue = cursor.execute("update accessrequest set status='accept' where  s_id='"+req_id+"' ")
        conn.commit()
        if resultvalue > 0:
            #SMTP.EmailSending.send_email("", "Access Activation Response","Your Search Request Activated from the cloud server", email)
            send_email("Access Activation Response", "Your Search Request Activated from the Administrator", email)
            alert(text='Request Accepted Success ', title='Request STATUS', button='OK')
            return useraccessreq()
        else:
            alert(text='Request Accepted Fails ', title='Request STATUS', button='OK')
            return useraccessreq()



@app.route('/userviewFiles')
def userviewFiles():
    userId = session['user_id']
    username = session['username']
    resultvalue = cursor.execute("select * from accessrequest where status='accept' and searchby='" + username + "'")
    conn.commit()
    details = cursor.fetchall()
    if resultvalue > 0:
        resultvalue = cursor.execute("select * from files")
        conn.commit()
        userDetails = cursor.fetchall()
        if resultvalue > 0:
            return render_template('userviewfiles.html', userDetails=userDetails)
        else:
            alert(text='File Uploded Details are not Available', title='File STATUS', button='OK')
            return render_template('userHome.html')
    else:
        alert(text='Your Dont Have the premission to view files into cloud ', title='Request STATUS', button='OK')
        return render_template('userHome.html')


@app.route('/request')
def request1():
        req_id=request.args.get('id')
        filename=request.args.get('filename')
        username = session['username']
        fkey = random.randint(500, 455000)
        ownername =request.args.get('ownername')
        resultvalue = cursor.execute("insert into request(file_id,filename,reqby,ownername,datee,fkey) values('"+req_id+"','"+filename+"','"+username+"','"+ownername+"',now(), '"+str(fkey)+"') ")
        conn.commit()
        if resultvalue > 0:
            alert(text='Request sent Success', title='Request STATUS', button='OK')
            return requestedFiles()
        else:
            alert(text='Request sent Fails', title='Request STATUS', button='OK')
            return render_template('userHome.html')

@app.route('/viewRequest')
def viewRequest():
    resultvalue = cursor.execute("select * from request where ownername='"+session['username']+"'")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('viewreqfiles.html', userDetails=userDetails)
    else:
        alert(text='File Request Details are onot Available', title='File STATUS', button='OK')
        return render_template('ownerHome.html')


@app.route('/acceptreqAccess')
def acceptreqAccess():
        req_id=request.args.get('id')
        reqby=request.args.get('reqby')
        query=cursor.execute("select * from uregistration where username='"+reqby+"'")
        conn.commit()
        querydetails=cursor.fetchall()
        letters = string.ascii_lowercase
        keyy = ''.join(random.choice(letters) for i in range(10))
        for a in querydetails:
            email=a[3]
            x=cursor.execute("select * from request where r_id='"+req_id+"'")
            conn.commit()
            xd=cursor.fetchall()
            for m in xd:
                fid=m[0]
                fileid=m[1]
                print("file id is"+fileid)
                v = cursor.execute("select * from files where fname='" + fileid + "'")
                vd=cursor.fetchall()
                for s in vd:

                    keyy=m[7]
                    resultvalue = cursor.execute("update request set status='accept' where  r_id='"+req_id+"' ")
                    conn.commit()
                    if resultvalue > 0:
                            #SMTP.EmailSending.send_email("","DAC Request Activation Response", "Use This Key for Download "+fileid+" File"+" :"+keyy,email)
                            send_email("Key Request Activation Response","Use This Key for Download "+str(fileid)+" File"+" :"+str(keyy) , email)
                            alert(text='Request Accepted Success', title='Request STATUS', button='OK')
                            return viewRequest()
                    else:
                        alert(text='Request Accepted Fails', title='Request STATUS', button='OK')
                        return viewRequest()

@app.route('/requestedFiles')
def requestedFiles():
    username = session['username']
    resultvalue = cursor.execute("select * from request where reqby='"+username+"' ")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('userreqfiles.html', userDetails=userDetails)
    else:
        alert(text='File Request Details are not Available', title='File STATUS', button='OK')
        return render_template('userHome.html')


@app.route('/download')
def download():
    id=request.args.get('id')
    return render_template('download.html',fileid=id)

@app.route('/download1')
def download1():
    id=request.args.get('fileid')
    key = request.args.get('key')
    username=session['username']
    letters = string.ascii_lowercase
    keyy = ''.join(random.choice(letters) for i in range(10))
    print("select * from files where keyy='"+key+"' and f_id='"+id+"'")
    a=cursor.execute("select * from request where fkey='"+key+"' and file_id='"+id+"'")
    resultvalue = cursor.fetchall()
    conn.commit()
    if a > 0 :
        for roww in resultvalue:
            oname =  roww[4]
            cursor.execute(
                "insert into download(user,filename,datee,ownername)values('" + username + "','" + roww[1] + "',now(),'" + roww[4] + "')")
            conn.commit()
            a = cursor.execute("select * from files where f_id='" + id + "'")
            resultvalue2 = cursor.fetchall()
            for roww in resultvalue2:
                # Decryption
                rest = Rest()
                result = rest.get('files/' + oname + '/' + roww[1])
                myEncrypted = result['fragment1'] + result['fragment2'] + result['fragment3'] + result['fragment4'] + result['fragment5'] + result['fragment6'] + result['fragment7']
                print(len(myEncrypted))
                print(len(roww[14]))
                myPlainText = None
                aeskey = bytes(roww[8], encoding='UTF-8')
                aesdataTuple = (bytes(roww[9],encoding='UTF-8'), bytes(roww[10],encoding='UTF-8'), bytes(roww[11],encoding='UTF-8'))
                myiv = bytes(roww[12], encoding='UTF-8')
                mykey = bytes(roww[13], encoding='UTF-8')
                #myEncrypted = bytes(roww[14], encoding='UTF-8')
                myEncrypted = bytes(myEncrypted, encoding='UTF-8')

                aeskey = binascii.unhexlify(aeskey)
                aesdataTuple = (binascii.unhexlify(aesdataTuple[0]), binascii.unhexlify(aesdataTuple[1]), binascii.unhexlify(aesdataTuple[2]))
                myiv = binascii.unhexlify(myiv)
                mykey = binascii.unhexlify(mykey)
                myEncrypted = binascii.unhexlify(myEncrypted)
                print(aeskey)
                print(aesdataTuple)
                print(myiv)
                print(mykey)
                print(myEncrypted)
                if roww[6] == 'TrippleDesk':
                    myTrippleDsk = MyTrippleDesk()
                    myPlainText = myTrippleDsk.decrypt_trippleDesk(myiv, mykey, myEncrypted)
                else:
                    myBlowfish = MyBlowFish()
                    myPlainText = myBlowfish.decrypt_blowfish(myiv, mykey, myEncrypted)
                myaes = MyAES()
                aesdataTupleNew = (myPlainText, aesdataTuple[1], aesdataTuple[2])
                aesPlaintext = myaes.decrypt_AES_GCM(aesdataTupleNew, aeskey)
                print(aesPlaintext)
                aesPlaintext = aesPlaintext.decode(encoding='UTF-8')
                csv = aesPlaintext.replace("\\r\\n", "\n")
                return Response(
                    csv,
                    mimetype="text/csv",
                    headers={"Content-disposition":
                                 "attachment; filename="+roww[1]+".txt"})
    else:
        alert(text='Please Enter Valid Key', title='File STATUS', button='OK')
        return render_template('userHome.html')


@app.route('/viewDownloaddetails')
def viewDownloaddetails():
    username=session['username']
    a=cursor.execute("select * from download where user='"+username+"'")
    details=cursor.fetchall()
    if a > 0:
        return  render_template('viewmydownloads.html',mydetails=details)
    else:
        alert(text='File Downloded Details are not Available', title='File STATUS', button='OK')
        return render_template('userHome.html')

@app.route('/aviewDownloaddetails')
def aviewDownloaddetails():
    a=cursor.execute("select * from download ")
    details=cursor.fetchall()
    if a > 0:
        return  render_template('aviewmydownloads.html',mydetails=details)
    else:
        alert(text='File Downloded Details are not Available', title='File STATUS', button='OK')
        return adminhome()


@app.route('/cviewDownloaddetails')
def cviewDownloaddetails():
    a=cursor.execute("select * from download ")
    details=cursor.fetchall()
    if a > 0:
        return  render_template('cviewmydownloads.html',mydetails=details)
    else:
        alert(text='File Downloded Details are not Available', title='File STATUS', button='OK')
        return render_template('cloudHome.html')


@app.route('/cviewuplodedfiles')
def cviewuplodedfiles():
    resultvalue = cursor.execute("select * from files")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('cviewfiles.html', userDetails=userDetails)
    else:
        alert(text='File Uploded Details are not Available', title='File STATUS', button='OK')
        return render_template('cloudHome.html')


@app.route('/cviewusers')
def cviewusers():
    image_names = os.listdir('./images')
    resultvalue = cursor.execute("select * from uregistration")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('cllusers.html', userDetails=userDetails)
    else:
        alert(text='Users details are not available', title='Details STATUS', button='OK')
        return render_template('cloudHome.html')


@app.route('/cviewowners')
def cviewowners():
    image_names = os.listdir('./images')
    resultvalue = cursor.execute("select * from Oregistration")
    conn.commit()
    userDetails = cursor.fetchall()
    if resultvalue > 0:
        return render_template('cllowners.html', userDetails=userDetails)
    else:
        alert(text='Users details are not available', title='Details STATUS', button='OK')
        return render_template('cloudHome.html')

@app.route('/oviewDownloaddetails')
def oviewDownloaddetails():
    a=cursor.execute("select * from download where ownername='"+session['username']+"' ")
    details=cursor.fetchall()
    if a > 0:
        return  render_template('oviewmydownloads.html',mydetails=details)
    else:
        alert(text='File Downloded Details are not Available', title='File STATUS', button='OK')
        return render_template('ownerHome.html')


if __name__ == '__main__':
    app.run(debug=True)

