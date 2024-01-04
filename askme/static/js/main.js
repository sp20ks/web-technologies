const items = document.getElementsByClassName('like-section')
const answer_like_section = document.getElementsByClassName('like-container')
const right_answer = document.getElementsByClassName('more-info')

function getCSRFToken() {
    // Extract the CSRF token from the cookie
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];

    return cookieValue;
}

const question_like_url = "/question_like";
const answer_like_url = "/answer_like"
const right_answer_url = "/right_answer"

const csrfToken = getCSRFToken();

// question_like
for (let item of items) {
    const [buttonLike, buttonDislike, text, counter] = item.children;
    buttonLike.addEventListener('click', () => {
        const headers = new Headers({
            'X-CSRFToken': csrfToken,
        });

        const formData = new FormData();
        formData.append('question_id', buttonLike.dataset.id);
        formData.append('value', buttonLike.dataset.value);

        const request = new Request('/question_like', {
            method: 'POST',
            headers: headers,
            body: formData,
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                counter.innerHTML = data.count;
            });
    });
    buttonDislike.addEventListener('click', () => {
        const headers = new Headers({
            'X-CSRFToken': csrfToken,
        });

        const formData = new FormData();
        formData.append('question_id', buttonLike.dataset.id);

        const request = new Request('/question_like', {
            method: 'POST',
            headers: headers,
            body: formData,
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                counter.innerHTML = data.count;
            });
    });

}

// answer_like
for (let item of answer_like_section) {
    const [buttonLike, buttonDislike, text, counter] = item.children;
    buttonLike.addEventListener('click', () => {
        const headers = new Headers({
            'X-CSRFToken': csrfToken,
        });

        const formData = new FormData();
        formData.append('answer_id', buttonLike.dataset.id);
        formData.append('value', buttonLike.dataset.value);

        const request = new Request('/answer_like', {
            method: 'POST',
            headers: headers,
            body: formData,
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                counter.innerHTML = data.count;
            });
    });
    buttonDislike.addEventListener('click', () => {
        const headers = new Headers({
            'X-CSRFToken': csrfToken,
        });

        const formData = new FormData();
        formData.append('answer_id', buttonLike.dataset.id);

        const request = new Request('/answer_like', {
            method: 'POST',
            headers: headers,
            body: formData,
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                counter.innerHTML = data.count;
            });
    });

}

for (let item of right_answer) {
    const [right_answer_change] = item.children;
    right_answer_change.addEventListener('click', () => {
        const headers = new Headers({
            'X-CSRFToken': csrfToken,
        });

        const formData = new FormData();
        formData.append('question_id', right_answer_change.dataset.question_id);
        formData.append('answer_id', right_answer_change.dataset.answer_id);
        formData.append('value', right_answer_change.dataset.value);

        const request = new Request('/right_answer', {
            method: 'POST',
            headers: headers,
            body: formData,
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                right_answer_change.value = value
            });
    });
}
