let lis = document.querySelectorAll('.nav>a')
console.log(lis)
for (var i = 0; i < lis.length; i++) {
    lis[i].onclick = function(event) {
        let li = document.getElementsByClassName('active')[0]
        li.classList.remove('active')
        event.target.classList.add('active')
    }
}
