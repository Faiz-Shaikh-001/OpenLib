let container = document.getElementById('container')

toggle = () => {
    if (container) {
        container.classList.toggle('sign-in')
        container.classList.toggle('sign-up')
    }
}

setTimeout(() => {
    if (container) {
        container.classList.add('sign-in')
    }
}, 200)

let msgEl = document.querySelector('ul.messages')
if (msgEl && typeof gsap !== 'undefined') {
    gsap.from(msgEl, {
        y: -100,
        duration: 0.8,
        opacity: 0
    })

    gsap.to(msgEl, {
        y: -100,
        duration: 0.8,
        opacity: 0,
        delay: 3.5,
        onComplete: () => {
            msgEl.remove()
        }
    })
}
