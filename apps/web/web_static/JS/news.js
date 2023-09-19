let left = document.querySelector('.button_next')
let right = document.querySelector('.button_prev')
let dots = document.querySelectorAll('.dot')
let images = document.querySelector('.images')

let index = 0
let last = 0
let time

function position()
{
    images.style.left = (index * -100) + "%"
}

function add()
{
    last = index
    if(index >= dots.length - 1)
        index = 0;
    else index++
}

function desc()
{
    last = index
    if(index < 1) 
        index = dots.length -1
    else index--
}

function timer()
{
    time = setInterval(()=>{
        last = index
        index++
        desc()
        add()
        dot()
        position()
    }, 3000)
}

function dot()
{
    dots[last].style.backgroundColor = "#ccc"
    dots[last].style.width = "8px"
    dots[last].style.height = "8px"
    dots[last].style.borderRadius = "4px"
    dots[index].style.backgroundColor = "#fff"
    dots[index].style.width = "12px"
    dots[index].style.height = "12px"
    dots[index].style.borderRadius = "6px"
}

left.addEventListener('click',()=>{
    desc()
    position()
    dot()
    clearInterval(time)
    timer()
})

right.addEventListener('click',()=>{
    add()
    position()
    dot()
    clearInterval(time)
    timer()
})

timer()

var btn

btn = document.getElementsByClassName("btn-prev-next");
btn[0].innerHTML = "&gt;";
btn[1].innerHTML = "&lt;";
