from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from forms import UploadFileForm
from models import UploadFile
import os
from django.conf import settings

@login_required
def home(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadFile(file = request.FILES['file'])
            new_file.save()
            return HttpResponseRedirect(reverse('main:home'))
    else:
        form = UploadFileForm()
    filelist = UploadFile.objects.all()
    data = {'form': form, 'username': user.username, 'filelist': filelist}
#    data = {'form': form, 'username': user.username, 'filelist': os.listdir(settings.MEDIA_ROOT)}
    return render_to_response('main/index.html', data, context_instance=RequestContext(request))

def files_list(request):
    return render_to_response('main/index.html',{'total_files':os.listdir(settings.MEDIA_ROOT),
                                                 'path':settings.MEDIA_ROOT},
                                                 context_instance=RequestContext(request))

def download(request,file_name):
    file_path = settings.MEDIA_ROOT +'/'+ file_name
    file_wrapper = FileWrapper(file(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name) 
    return response

def delete(request):
    if request.method != 'POST':
        raise HTTP404
    docId = request.POST.get('file', None)
    docToDel = get_object_or_404(UploadFile, pk = docId)
    docToDel.file.delete()
    docToDel.delete()
#    return HttpResponseRedirect(reverse('main:home'))
    return render_to_response('main/index.html')
