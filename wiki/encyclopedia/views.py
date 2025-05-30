from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.urls import reverse
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

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()

        filename = f"entries/{title}.md"

        if default_storage.exists(filename):
            return render(request, "encyclopedia/create.html", {
                "message": f"The entry '{title}' already exists.",
                "title": title,
                "content": content
            })

        # save new entry
        default_storage.save(filename, ContentFile(content))

        # Redirect to the new entry page
        return redirect(reverse("entry_page", args=[title]))

    return render(request, "encyclopedia/create.html")


def edit(request, title):

    if request.method == "POST":
        new_title = request.POST["title"]
        new_content = request.POST["content"]
        util.save_entry(new_title, new_content)
        return redirect("entry_page", title=new_title)
    
    # GET request: Load the entry content and populate form
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Entry not found."
        })
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "title_value": title,  # pre-fill title field
        "content_value": content  # pre-fill textarea
    })