function filterInLibrary(button){
    let id = button.id;
    callAjaxGet(id, res => {
        let books = JSON.parse(res);
        console.log(books);
        for (let book of books){
            let card = document.getElementById(book.title);
            if (book.status === 'false'){
                card.style.display =  'none';
            } else if (book.status === 'true'){
                card.style.display = 'block';
            }
        }
    })
}

function callAjaxGet(id, callback){
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if(this.readyState === 4 && this.status === 200)
            callback(this.responseText);
    };
    xhttp.open("GET",`/library/${id}`,true);
    xhttp.send();
}

function callAjaxPost(id, callback){
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if(this.readyState === 4 && this.status === 200)
            callback(this.responseText);
    };
    xhttp.open("POST",'/give',true);
    xhttp.send();
}
