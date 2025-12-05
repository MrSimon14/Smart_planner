from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic,Note
from .forms import TopicForm, NoteForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404

def index(request):
    #home page
    topics_count = 0
    notes_count = 0
    
    if request.user.is_authenticated:
        # Считаем темы текущего пользователя
        topics_count = Topic.objects.filter(owner=request.user).count()
        
        # Считаем заметки текущего пользователя
        notes_count = Note.objects.filter(topic__owner=request.user).count()
    
    context = {
        'topics_count': topics_count,
        'notes_count': notes_count,
    }
    return render(request, 'smart_planner/index.html', context)
    

@login_required
def topics(request):
    #show list of topics
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'smart_planner/topics.html', context)

@login_required
def topic(request, topic_id):
    #show entries of 1 topic
    topic = Topic.objects.get(id = topic_id)
    if topic.owner != request.user:
        raise Http404
    notes = topic.note_set.order_by('-date_added')
    context = {'topic':topic, 'notes': notes}
    return render(request, 'smart_planner/topic.html', context)

@login_required
def new_topic(request):
    #add new theme
    if request.method  != 'POST':
        #create empty form
        form = TopicForm()
    else:
        #data was sent
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('smart_planner:topics')
    #show empty form:
    context = {'form':form}
    return render(request,'smart_planner/new_topic.html', context)

@login_required
def new_note(request, topic_id):
    #add a new note for current topic
    topic = Topic.objects.get(id = topic_id)

    if request.method != 'POST':
        #create empty form
        form = NoteForm()
    else:
        #data was sent
        form = NoteForm(data = request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.topic = topic
            new_note.save()
            return redirect('smart_planner:topic', topic_id = topic_id)
        
    #show empty or incorrect form
    context = {'topic': topic, 'form': form}
    return render(request, 'smart_planner/new_note.html',context)

@login_required
def edit_note(request, note_id):
    #edit the note
    note = Note.objects.get(id = note_id)
    topic = note.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #data from current note
        form = NoteForm(instance=note)
    else:
        #sent the data POST; add current data
        form =NoteForm(instance=note, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('smart_planner:topic', topic_id = topic.id)
        
    context = {'note': note, 'topic': topic, 'form': form}
    return render(request, 'smart_planner/edit_note.html', context)

@login_required
def delete_topic(request, topic_id):
    #delete the topic
    topic = get_object_or_404(Topic, id=topic_id)
    
    if request.method == 'POST':
        topic.delete()
        messages.success(request, 'Тема успешно удалена!')
        return redirect('smart_planner:topics')
    
    #show empty or incorrect form
    context = {'topic':topic}
    return render(request, 'smart_planner/delete_topic.html', context)

@login_required
def delete_note(request, note_id):
    #delete the note
    note = get_object_or_404(Note, id = note_id)
    topic = note.topic

    if topic.owner != request.user:
        raise Http404
    
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Заметка успешно удалена!')
        return redirect('smart_planner:topic',   topic_id = topic.id)
    
    #show empty or incorrect form
    context = {'topic':topic, 'note':note}
    return render(request, 'smart_planner/delete_note.html', context)

@login_required
def search_notes(request):
    notes = Note.objects.filter(topic__owner=request.user)
    query = None
    results = []
    
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            if query:
                # search notes 
                results = notes.filter(text__icontains=query).select_related('topic')
    else:
        form = SearchForm()
    
    context = {
        'form': form,
        'query': query,
        'results': results,
        'results_count': len(results)
    }
    return render(request, 'smart_planner/search.html', context)