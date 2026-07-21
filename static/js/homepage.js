gsap.registerPlugin(ScrollTrigger);

var tl = gsap.timeline();

tl.from("#logo svg, #logo h1, #nav-items > *", {
  y: -30,
  duration: 0.7,
  opacity: 0,
  stagger: 0.1,
  ease: "power2.out",
  onComplete: () => {
    gsap.set("#logo svg, #logo h1, #nav-items > *", { clearProps: "all" });
  }
});

tl.from("#Hero-text, #Hero-text h1", {
  y: 40,
  stagger: 0.2,
  opacity: 0,
  duration: 0.9,
  ease: "power2.out"
}, "-=0.3");

gsap.from("#page2 .container1, #page2 .container2", {
  y: 40,
  opacity: 0,
  stagger: 0.3,
  duration: 0.9,
  ease: "power2.out",
  scrollTrigger: {
    trigger: "#page2",
    start: "top 80%",
    toggleActions: "play none none none"
  }
});

gsap.from("#page3 .footer-container-1, #page3 .footer-container-2", {
  y: 30,
  opacity: 0,
  stagger: 0.3,
  duration: 0.8,
  ease: "power2.out",
  scrollTrigger: {
    trigger: "#page3",
    start: "top 85%",
    toggleActions: "play none none none"
  }
});

function openNav() {
  document.getElementById("mobile-menu").style.height = "100vh";
}

function closeNav() {
  document.getElementById("mobile-menu").style.height = "0";
}
