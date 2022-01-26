
export function loadPosts(callback){
    const xhr = new XMLHttpRequest()
    const method = "GET"
    const url = "http://127.0.0.1:8000/api/posts/"
    const responseType = "json"
    xhr.responseType = responseType
    xhr.open(method, url)
    xhr.onload = function() {
      callback(xhr.response, xhr.status)
    }
    xhr.onerror = function(e){
      callback({"message": "The request was an error"}, 400)
    }
    xhr.send()
  }