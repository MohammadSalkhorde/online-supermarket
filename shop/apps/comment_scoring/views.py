from django.shortcuts import render,get_object_or_404,redirect
from .forms import CommentForm
from .models import Comment,Scoring
from django.views import View
from apps.products.models import Product
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from django.db.models import Q

#==================================================================================
class CommentView(View):
    def get(self,request,*args, **kwargs):   
        productId=request.GET.get('productId')
        commentId=request.GET.get('commentId')
        slug=kwargs['slug']
        initial_dict={
            'product_id':productId,
            'comment_id':commentId
        }
        form=CommentForm(initial=initial_dict)
        
        context={
            'form':form,
            'slug':slug,
            'comment_id':commentId
        }
        
        return render(request,'cs/create_comment.html',context)
    
    def post(self,request,*args, **kwargs):
        form=CommentForm(request.POST)
        slug=kwargs['slug']
        if form.is_valid():
            cd=form.cleaned_data
            product=get_object_or_404(Product,slug=slug)
            parent=None
            if (cd['comment_id']):
                parentId=cd['comment_id']
                parent=Comment.objects.get(id=parentId)
                
            Comment.objects.create(
                product=product,
                commenting_user=request.user,
                comment_text=cd['comment_text'],
                comment_parent=parent
            )
            
            messages.success(request,'نظر شما با موفقیت ثبت شد')
            return redirect('products:product_detail',product.slug)
        
        messages.error(request,'خطا در ارسال نظر','danger')
        return redirect('products:product_detail',product.slug)
#==================================================================================
def add_score(request):
    productId=request.GET.get('productId')
    score=request.GET.get('score')
    
    product=Product.objects.get(id=productId)
    scoring=Scoring.objects.filter(Q(product=product) & Q(scoring_user=request.user))
    if scoring.exists():
        return False
    else:
        Scoring.objects.create(
            product=product,
            scoring_user=request.user,
            score=score
        )
    
    return JsonResponse({"average_score":product.get_average_score()})
#==================================================================================