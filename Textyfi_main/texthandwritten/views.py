from django.shortcuts import render
from PIL import Image
from fpdf import FPDF
from PIL import Image
import os
import requests
from .models import handwritten,texthand
from .forms import handwrittenForm
# Create your views here.
from os.path import expanduser
from wsgiref.util import FileWrapper
from django.http import HttpResponse
import mimetypes
gap, _ = 0, 0
BG = Image.open("media/myfont/bg.png")
sizeOfSheet = BG.width
       
allowedChars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,.-?!() 1234567890'
def writee(char):
        global gap, _
        if char != '\n':
            cases = Image.open("media/myfont/%s.png" % char.lower())
            BG.paste(cases, (gap, _))
            size = cases.width
            gap += size

def letterwrite(word):
        global gap, _
        if gap > sizeOfSheet - 95 * (len(word)):
            gap = 0
            _ += 200
        special_char = {'.':'fullstop','!':'exclamation','?':'question',',':'comma','(':'braketop', ')':'braketcl','-':'hiphen'}
        for letter in word:
            if letter in allowedChars:
                
                if letter.islower():
                    pass
                elif letter.isupper():
                    letter = letter.lower()
                    letter += 'upper'
                elif letter in special_char:
                    if special_char[letter] is not None:
                        letter = special_char[letter]
                writee(letter)


def worddd(Input):
        wordlist = Input.split(' ')
        for i in wordlist:
            letterwrite(i)
            writee('space')
def pdf_creation(PNG_FILE, flag=False):
        rgba = Image.open(PNG_FILE)
        rgb = Image.new('RGB', rgba.size, (255, 255, 255))  # white background
        rgb.paste(rgba, mask=rgba.split()[3])  # paste using alpha channel as mask
        rgb.save('media/outputs/output.pdf',
                append=flag)
def textsen(request,sentence):
    sentence1=sentence
    thand=texthand.objects.create(sentence=sentence1).save()
    return HttpResponse(str(sentence))
def texthandview(request):
   
    sentence=texthand.objects.all()
    if request.method == 'POST':
        global BG
        res=request.POST
        sentence=res['sentence']
        res=requests.get('http://localhost:8000/textsen/'+ sentence)
        data=res.text
        with open('media/outputs/output.pdf', 'w') as file:
            pass

        l = len(data)
        nn = len(data) // 600
        chunks, chunk_size = len(data), len(data) // (nn + 1)
        p = [data[i:i + chunk_size] for i in range(0, chunks, chunk_size)]

        for i in range(0, len(p)):
            worddd(p[i])
            writee('\n')
            BG.save('%doutt.png' % i)
            BG1 = Image.open("media/myfont/bg.png")
            BG = BG1
            gap = 0
            _ = 0
           

        imagelist = []
        for i in range(0, len(p)):
            imagelist.append('%doutt.png' % i)


        pdf_creation(imagelist.pop(0))

        
        for PNG_FILE in imagelist:
            pdf_creation(PNG_FILE, flag=True)
                
       
        # return render(request,'app/texthand.html',{'form':form})
        temp={'sentence':sentence}
        
    else:
        temp={'sentence':"Enter text"}
    return render(request,'app/texthand.html',temp)




    

def texthandwritten(request):
        
    if request.method=='POST':
        name1=handwritten(textfile=request.POST)
        form=handwrittenForm(request.POST,request.FILES)
        if form.is_valid():
            document=form.save(commit=False)
            document.name='boom.txt'
            document.save()
            global BG
            try:
                with open('media/text/boom.txt', 'r') as file:
                    data = file.read().replace('\n', '')

                with open('media/outputs/output.pdf', 'w') as file:
                    pass

                l = len(data)
                nn = len(data) // 600
                chunks, chunk_size = len(data), len(data) // (nn + 1)
                p = [data[i:i + chunk_size] for i in range(0, chunks, chunk_size)]

                for i in range(0, len(p)):
                    worddd(p[i])
                    writee('\n')
                    BG.save('%doutt.png' % i)
                    BG1 = Image.open("media/myfont/bg.png")
                    BG = BG1
                    gap = 0
                    _ = 0
            except ValueError as E:
                print("{}\nTry again".format(E))

            imagelist = []
            for i in range(0, len(p)):
                imagelist.append('%doutt.png' % i)

        
            pdf_creation(imagelist.pop(0))

            
            for PNG_FILE in imagelist:
                pdf_creation(PNG_FILE, flag=True)
            return render(request,'app/texthand.html')
    else:
        form=handwrittenForm()
    return render(request,'app/texthand.html',{'form':form})
def download(request):
    path = expanduser('~/outputs/')
    wrapper = FileWrapper(open("media/outputs/output.pdf",'rb'))
    response = HttpResponse(wrapper, content_type=mimetypes.guess_type('output.pdf')[0])
    response['Content-Length'] = os.path.getsize("media/outputs/output.pdf")
    response['Content-Disposition'] = "attachment" + 'output.pdf'
    return response