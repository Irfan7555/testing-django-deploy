
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from supabase_client import supabase


def home(request):
    try:
        response = (
            supabase.table("tasks")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        tasks = response.data

    except Exception as e:
        tasks = []
        messages.error(request, f"Unable to load tasks: {e}")

    return render(request, "todo/home.html", {"tasks": tasks})


@require_POST
def add_task(request):
    title = request.POST.get("title", "").strip()

    if not title:
        messages.error(request, "Task title cannot be empty.")
        return redirect("home")

    try:
        supabase.table("tasks").insert({
            "title": title,
            "completed": False
        }).execute()

        messages.success(request, "Task added successfully!")

    except Exception as e:
        messages.error(request, f"Unable to add task: {e}")

    return redirect("home")


@require_POST
def complete_task(request, task_id):
    try:
        response = (
            supabase.table("tasks")
            .select("completed")
            .eq("id", task_id)
            .execute()
        )

        if not response.data:
            messages.error(request, "Task not found.")
            return redirect("home")

        current_status = response.data[0]["completed"]

        supabase.table("tasks").update({
            "completed": not current_status
        }).eq("id", task_id).execute()

        messages.success(request, "Task status updated!")

    except Exception as e:
        messages.error(request, f"Unable to update task: {e}")

    return redirect("home")


@require_POST
def delete_task(request, task_id):
    try:
        supabase.table("tasks").delete().eq(
            "id", task_id
        ).execute()

        messages.success(request, "Task deleted successfully!")

    except Exception as e:
        messages.error(request, f"Unable to delete task: {e}")

    return redirect("home")
