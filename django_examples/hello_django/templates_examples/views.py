from django.shortcuts import render

# Create your views here.
class Post:

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def length(self):
        return len(self.content)


    def present(self):
        html = f"""
        <h2>{self.title}</h2>
        <p>{self.content}</p>
        """
        return html

def example(request):
    context = {}
    context['text'] = 'Hello from Django'
    context['liczba_int'] = 123
    context['liczba_float'] = 123.456
    context["lista"] = ["A", "B", "C"]
    context["imiona"] = ["Jan", "Piotr", "Ania", "Gosia", "Krzysztof"]

    messages = {"success": ["Jest ok"], "info": ["Kawa gotowa", "Temperatura 19 stopni"]}

    context["messages"] = messages

    post = Post("Pierwszy post", "To jest pierwszy post na blogu")
    context["post"] = post


    return render(
        request=request,
        template_name='templates_examples/example.html',
        context=context
    )