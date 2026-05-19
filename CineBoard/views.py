from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_list_or_404, redirect
from .models import Movie, Genre, Comment, VipBooking
from .forms import CommentForm, VipBookingForm

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'CineBoard/register.html'
    success_url = reverse_lazy('login')

class MyLoginView(LoginView):
    template_name = 'CineBoard/login.html'
    def get_success_url(self):
        return reverse_lazy('movie_list')

class MyLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class MovieListView(generic.ListView):
    model = Movie
    template_name = 'CineBoard/movie_list.html'
    context_object_name = 'movies'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset() 
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
            
        genre_id = self.request.GET.get('genre')
        if genre_id:
            queryset = queryset.filter(genres__id=genre_id)
            
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        return context



class MovieDetailView(generic.DetailView):
    model = Movie
    template_name = 'CineBoard/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['booking_form'] = VipBookingForm()
        context['comments'] = self.object.comments.all().order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
            
        self.object = self.get_object()
        
        if 'submit_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.movie = self.object
                comment.user = request.user
                comment.save()
                return redirect(reverse('movie_detail', kwargs={'pk': self.object.pk}))
                
        elif 'submit_booking' in request.POST:
            if VipBooking.objects.filter(user=request.user).exists():
                return redirect(reverse('movie_detail', kwargs={'pk': self.object.pk}) + '?error=already_booked')
                
            booking_form = VipBookingForm(request.POST)
            if booking_form.is_valid():
                booking = booking_form.save(commit=False)
                booking.movie = self.object
                booking.user = request.user
                booking.save()
                return redirect(reverse('movie_detail', kwargs={'pk': self.object.pk}))

        return redirect(reverse('movie_detail', kwargs={'pk': self.object.pk}))

class MovieCreateView(LoginRequiredMixin, generic.CreateView):
    model = Movie
    template_name = 'CineBoard/movie_form.html'
    fields = ['title', 'description', 'release_date', 'genre', 'rating', 'release_year', 'duration', 'budget']
    success_url = reverse_lazy('movie_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class MovieUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Movie
    template_name = 'CineBoard/movie_form.html'
    fields = ['title', 'description', 'release_date', 'genre', 'rating', 'release_year', 'duration', 'budget']
    
    def get_success_url(self):
        return reverse_lazy('movie_detail', kwargs={'pk': self.object.pk})

class MovieDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Movie
    template_name = 'CineBoard/movie_confirm_delete.html'
    success_url = reverse_lazy('movie_list')