// Search questions system
const questionsSearch = () => {
    
    const search_input = document.getElementById("searchInput").value

    if (search_input != ""){

        window.location.replace(`/questions/search?q=${search_input}`)

    }

}

// Search books system
const booksSearch = () => {
    
    const search_input = document.getElementById("searchInput").value

    if (search_input != ""){

        window.location.replace(`/books/search?q=${search_input}`)

    }

}