from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

body = '''
The official release date of Spider-Man: Across the Spider-Verse has been announced, indicating when the film will begin streaming on Netflix.

Since the COVID-19 pandemic, release windows for films in theaters have shrunk significantly, and completely disappeared in many cases.

As for Sony Pictures, a studio without a direct-to-consumer streaming service, its strategy is different than many others like Disney, Paramount, Warner Bros. Discovery, and NBC Universal.

Sony has a relatively new streaming deal, where in essence, its films head to Netflix first for 18 months, then leave that streamer to be available on Disney+.
'''


class Tags:
    def __init__(self, tag_id, name):
        self.id = tag_id
        self.name = name


class Answer:
    def __init__(self, answer_id, content, rating):
        self.id = answer_id
        self.content = content
        self.rating = rating


class Question:
    def __init__(self, question_id, title, content, rating, author_img, tags: list, answers: list):
        self.id = question_id
        self.title = title
        self.content = content
        self.rating = rating
        self.author_img = author_img
        self.tags = tags
        self.answers = answers


def create_question_item(
        question_id: int,
        title: str,
        content: str,
        rating: int,
        tags: list = [],
        answers: list = [],
        author_img: str = 'https://sun9-74.userapi.com/impg/IkdqPKOIfRr8TF5XrDpx0FApStrqI3N00iDHmw/McWp1do3_sU.jpg?size=1080x1080&quality=95&sign=050a9d0bbcbb22084f2f41f5574b7c71&type=album',
) -> Question:
    return Question(
        question_id,
        title,
        content,
        rating,
        author_img,
        tags,
        answers,
    )


questions = [
    create_question_item(
        i,
        f'Sample title {i}',
        body,
        100 + i,
        [Tags(tag, f'tag {tag}') for tag in range(i)],
        [
            Answer(answer, f'Answer №{answer}. Something about post', 10 + answer)
            for answer in range(3)
        ]
    )
    for i in range(40)
]


# MARK: - Routing

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    page_obj = paginate(questions, request, 5)
    return render(request, 'index.html', {
        'title': 'New Questions',
        'questions': questions[page_obj.start_index() - 1: page_obj.end_index()],
        'page_obj': page_obj,
    })


def ask_question(request):
    return render(request, 'ask_question.html')


def settings(request):
    return render(request, 'settings.html')


def login(request):
    return render(request, 'login.html')


def hot_list(request):
    filtered_questions = list(filter(lambda q: q.rating > 130, questions))
    page_obj = paginate(filtered_questions, request, 5)
    return render(request, 'index.html', {
        'title': 'Hot Questions',
        'questions': filtered_questions[page_obj.start_index() - 1: page_obj.end_index()],
        'page_obj': page_obj,
    })


def tag_list(request, tag):
    filtered_questions = list(filter(lambda q: tag in [t.name for t in q.tags], questions))
    page_obj = paginate(filtered_questions, request, 5)
    return render(request, 'index.html', {
        'title': f'Questions with tag: "{tag}"',
        'questions': filtered_questions[page_obj.start_index() - 1: page_obj.end_index()],
        'page_obj': page_obj,
    })


def signup(request):
    return render(request, 'signup.html')


def question(request, question_id):
    question_item = questions[question_id]
    return render(request, 'question.html', {'question': question_item})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")
