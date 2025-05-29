from django.shortcuts import render
from django.shortcuts import redirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    content = util.get_entry(title)

    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"The entry '{title}' was not found."
        })
    
    
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })


def search(request):
    query = request.GET.get('q', '').strip()
    entries = util.list_entries()
    

    if not query:
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "results": []
        })

   # Exact match (case-insensitive)
    for entry in entries:
        if entry.lower() == query.lower():
            return redirect('entry_page', title=entry)
    
    # partial match (case-insensitive)
    results = [entry for entry in entries if query.lower() in entry.lower()]
    
    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "results": results
    })

def create(request):

    return render(request, "encyclopedia/create.html", {
        "message": "This feature is not implemented yet."
    })