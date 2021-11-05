let input_search = document.getElementById('searching')
const search_form = document.getElementById("search_form")
input_search.addEventListener("keyup", debounce(searchChange, 400))


function debounce(cb, interval, immediate) {
    var timeout;

    return function () {
        var context = this, args = arguments;
        var later = function () {
            timeout = null;
            if (!immediate) cb.apply(context, args);
        };

        var callNow = immediate && !timeout;

        clearTimeout(timeout);
        timeout = setTimeout(later, interval);

        if (callNow) cb.apply(context, args);
    };
};

async function searchChange(e) {
    const ul = document.getElementById('search_hints')
    const value = e.target.value
    if (value === "") {
        ul.style.display = "none"
        return
    }
    const baseUrl = `${location.origin}/search_hints/?search=${value}`
    let res = await fetch(baseUrl, {
        method: "GET",
    })
    res = await res.json()
    const clickHandler = (item) => {
        input_search.value = item
        search_form.submit()
    }
    ul.innerHTML = ""

    if (res.employees.length) {
        ul.style.display = "block"
    } else {
        ul.style.display = "none"
    }

    res.employees.forEach((item) => {
        const li = document.createElement('li')
        li.classList = ['searching__hinting-item']
        li.innerText = item
        li.onclick = () => clickHandler(item)
        ul.appendChild(li)
    })

}