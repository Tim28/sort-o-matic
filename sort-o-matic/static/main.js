$('a#search').on("click", function () {
    const searchValue = $('#search_input').val();
    search(searchValue);
});

$('input#search_input').on('keypress', function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("search").click();
    }
})

// $('body').on('keypress', function (event) {
//     const searchInput = $('input#search_input');
//
//     if (event.key === "s" && !searchInput.is(':focus')) {
//         event.preventDefault()
//         searchInput.focus();
//     }
// })

function search(value) {
    console.log(value);
    window.location.href = `/search?value=${value}`
}

function redirect(code) {
    window.location.href = `/scan/${code}`;
}

function onScanSuccess(decodedText, decodedResult) {
    // handle the scanned code as you like, for example:
    console.log(`Code matched = ${decodedText}`, decodedResult);
    redirect(decodedText);
}

function onScanFailure(error) {
    // handle scan failure, usually better to ignore and keep scanning.
    // for example:
    //console.warn(`Code scan error = ${error}`);//
}
