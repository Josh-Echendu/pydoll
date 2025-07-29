
// Step 1: Select the element
let checkbox = document.querySelector("input[name='agree']")

// Step 2: Inspect all event listeners
getEventListeners(checkbox)

//See the Source of the Listener
getEventListeners(checkbox).click[0].listener.toString()

//🕵️ Pro Debug Strategy:

// Step 1: Start from the checkbox
let el = document.querySelector("input[name='agree']")

// Step 2: Climb up the DOM tree and check each
while (el) {
    console.log("Checking:", el)
    console.log(getEventListeners(el))
    el = el.parentElement
}
