# Create your views here.
from django.http import HttpResponse
from phillyleg.models import Subscription,KeywordSubscription,LegFile,CouncilMember,CouncilMemberSubscription
from django.template import Context, loader

def index(request):
    t = loader.get_template('subscribe.html')
    c = Context({
    	'council_members': CouncilMember.objects.all()
    })
    return HttpResponse(t.render(c))

def create(request):
    emailvar = request.POST['email']
    s = Subscription(email = emailvar)
    s.save()
    keywords = request.POST['keywords']
    keylist = keywords.split(",") 
    for word in keylist:
        k = KeywordSubscription(keyword = word, subscription = s)
        k.save()
    members = request.POST.getlist('council')
    ret_members = []
    for mem in members:
    	cmember = CouncilMember.objects.get(id=mem)
    	ret_members.append(cmember)
        cm = CouncilMemberSubscription(councilmember = cmember, subscription = s)
        cm.save()
    t = loader.get_template('received.html')
    c = Context({
        'emailvar': emailvar,
        'keylist': keylist,
        'members': ret_members
    })
    return HttpResponse(t.render(c))

def unsubscribe(request):
    t = loader.get_template('editsubscribe.html')
    c = Context()
    return HttpResponse(t.render(c))

def delete(request):
    t = loader.get_template('unsubscribed.html')
    emailvar = request.POST['email']
    s = Subscription.objects.filter(email = emailvar)
    for item in s:
        item.delete()
    c = Context({
        'email': emailvar
    })
    return HttpResponse(t.render(c))

