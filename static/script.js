

const Questions = [{
    id: 0,
    q: "What is capital of India?",
    a: [{ text: "gandhinagar", isCorrect: false },
        { text: "Surat", isCorrect: false },
        { text: "Delhi", isCorrect: true },
        { text: "mumbai", isCorrect: false }
    ]

},
{
    id: 1,
    q: "What is the capital of Thailand?",
    a: [{ text: "Lampang", isCorrect: false, isSelected: false },
        { text: "phuket", isCorrect: false },
        { text: "Ayutthaya", isCorrect: false },
        { text: "Bangkok", isCorrect: true }
    ]

},
{
    id: 2,
    q: "What is the capital of Gujarat",
    a: [{ text: "surat", isCorrect: false },
        { text: "vadodara", isCorrect: false },
        { text: "gandhinagar", isCorrect: true },
        { text: "rajkot", isCorrect: false }
    ]

}

]

// Set start
var start = true;

// Iterate
function iterate(id) {

// Getting the result display section
var result = document.getElementsByClassName("result");
result[0].innerText = "";

// Getting the question
const question = document.getElementById("question");


// Setting the question text
question.innerText = Questions[id].q;

// Getting the options
const op1 = document.getElementById('op1');
const op2 = document.getElementById('op2');
const op3 = document.getElementById('op3');
const op4 = document.getElementById('op4');


// Providing option text 
op1.innerText = Questions[id].a[0].text;

op2.innerText = Questions[id].a[1].text;
op3.innerText = Questions[id].a[2].text;
op4.innerText = Questions[id].a[3].text;

// Providing the true or false value to the options
op1.value = Questions[id].a[0].isCorrect;
op2.value = Questions[id].a[1].isCorrect;
op3.value = Questions[id].a[2].isCorrect;
op4.value = Questions[id].a[3].isCorrect;

var selected = "";

// Show selection for op1
op1.addEventListener("click", () => {
    op1.style.backgroundColor = "green";
    op2.style.backgroundColor = "white";
    op3.style.backgroundColor = "white";
    op4.style.backgroundColor = "white";
    
    selected = op1.value;
})

// Show selection for op2
op2.addEventListener("click", () => {
    op1.style.backgroundColor = "white";
    op2.style.backgroundColor = "green";
    op3.style.backgroundColor = "white";
    op4.style.backgroundColor = "white";
    
    
    selected = op2.value;
})

// Show selection for op3
op3.addEventListener("click", () => {
    op1.style.backgroundColor = "white";
    op2.style.backgroundColor = "white";
    op3.style.backgroundColor = "green";
    op4.style.backgroundColor = "white";
    
    selected = op3.value;
})

// Show selection for op4
op4.addEventListener("click", () => {
    op1.style.backgroundColor = "white";
    op2.style.backgroundColor = "white";
    op3.style.backgroundColor = "white";
    op4.style.backgroundColor = "green";
    selected = op4.value;
})

// Grabbing the evaluate button
const evaluate = document.getElementsByClassName("evaluate");

}

if (start) {
iterate("0");
}

// Next button and method
const next = document.getElementsByClassName('next')[0];
var id = 0;

next.addEventListener("click", () => {
start = false;
if (id < 2) {
    id++;
    iterate(id);
    op1.style.backgroundColor = "white";
    op2.style.backgroundColor = "white";
    op3.style.backgroundColor = "white";
    op4.style.backgroundColor = "white";
}
else{
    question.innerText = "No More Questions! \n You can press on submit";
    document.getElementById('option-container').style.display='none';
    document.getElementById('next').style.display='none';
}
})