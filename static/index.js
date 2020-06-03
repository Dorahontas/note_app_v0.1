// the function get the user name from the html form and puts it into the localStorage
function registerUser() {
  var userName = document.getElementById('register_input').value  // get the name specified by the user

  localStorage.setItem('username', userName) // set the key:value pair in the localStorage

  displayPage() // call the displayPage function
}

// the function displays either the 'welcome user' or the 'registration' page depending on the presence of the username in the localStorage
function displayPage() {
  const userName = localStorage.getItem('username') // get the 'username' from the localStorage

  const registrationPage = document.getElementById('registration') // get the div element with id 'registration'
  const helloPage = document.getElementById('hello') // get the div element with id 'hello'

  if (userName === null) {
    // if there is no username in the localSorage show the registration page
    registrationPage.hidden = false
    helloPage.hidden = true
  } else {
    // else show the hello user page, because the username is already present in the localStorage
    registrationPage.hidden = true
    helloPage.hidden = false

    // change the text welcome text by adding the user name
    document.getElementById('username').innerHTML = 'Welcome, ' + userName
  }
}

const submitButton = document.getElementById('register_button') // get the registration button with id 'register_button'
// register the click event of the registration button to the registerUser function
submitButton.addEventListener('click', registerUser)

displayPage() // call the function displayPage
