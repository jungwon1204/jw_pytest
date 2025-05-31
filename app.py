from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

problems = [
    {
        "id": 1,
        "code": 'print("Hello, Python!")\nprint(5 + 7)',
        "answer": 'Hello, Python!\n12',
        "concept": "문자열 출력과 정수 덧셈"
    },
    {
        "id": 2,
        "code": 'a = 3\nb = 4\nprint(a * b)',
        "answer": '12',
        "concept": "변수 선언과 곱셈 연산"
    },
    {
        "id": 3,
        "code": 'for i in range(2):\n    print("Hi")',
        "answer": 'Hi\nHi',
        "concept": "반복문 for와 range"
    },
    {
        "id": 4,
        "code": 'print("A" * 3)',
        "answer": 'AAA',
        "concept": "문자열과 숫자의 곱 → 문자열 반복"
    },
    {
        "id": 5,
        "code": 'print(7 // 2)',
        "answer": '3',
        "concept": "정수 나눗셈 연산자 //"
    },
    {
        "id": 6,
        "code": 'print(len("Python"))',
        "answer": '6',
        "concept": "문자열 길이 구하기 (len)"
    },
]

@app.route("/")
def index():
    solved_ids = session.get("solved_ids", [])
    remaining = [p for p in problems if p["id"] not in solved_ids]

    if not remaining:
        return """
        <div style='text-align:center; margin-top:100px; font-family:sans-serif'>
            <h2>🎉 모든 문제를 풀었습니다!</h2>
            <p><a href='/reset'>처음부터 다시 시작하기</a></p>
        </div>
        """

    problem = random.choice(remaining)
    session["last_problem"] = problem
    return render_template("index.html", code=problem["code"], answer=problem["answer"])

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    user_answer = data.get("user_answer", "").strip()
    correct_answer = data.get("correct_answer", "").strip()

    is_correct = user_answer == correct_answer
    concept = None

    if is_correct:
        last = session.get("last_problem")
        if last:
            concept = last.get("concept", "")
            solved = session.get("solved_ids", [])
            if last["id"] not in solved:
                solved.append(last["id"])
                session["solved_ids"] = solved

    return jsonify({"result": is_correct, "concept": concept})

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
