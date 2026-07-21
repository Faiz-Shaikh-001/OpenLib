function openNav() {
    document.getElementById("mobile-menu").style.height = "100%";
}

function closeNav() {
    document.getElementById("mobile-menu").style.height = "0";
}

gsap.from('ul.messages', {
    y: -200,
    duration: 1
})

gsap.to('ul.messages', {
    y: -200,
    duration: 1,
    delay: 6
})