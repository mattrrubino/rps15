import './CreateAccount.css'
import { useNavigate } from "react-router-dom"

const CreateAccount = () => {
  const navigate = useNavigate()

  function onSubmit() {
        const password = document.getElementById("password").value
        const passwordAgain = document.getElementById("password-again").value

        if (password != passwordAgain) {
          alert("Passwords do not match.")
          return
        }

        var xhr = new XMLHttpRequest()
        xhr.open("POST", "/api/register")

        xhr.onreadystatechange = (e) => {
          console.log(e)
            if (xhr.readyState != XMLHttpRequest.DONE) {
                return
            }

            const status = xhr.status;
            if (status === 201) {
                navigate("/")
            } else if (status === 409) {
                alert("Username already registered.")
            } else {
                alert("Username must have 1-32 characters and password must have 8-32 characters.")
            }
        }

        var formData = new FormData(document.getElementById("create-account-form"))
        xhr.send(formData)
  }

  return (
    <div>
      <div className="create-account-container">
        <div className="create-flex-container">

          <div className="flex-item">
            <div className="logo">Account Create</div>
          </div>

          <br/>

          <form className="create-account-form" id="create-account-form">
            <div className="flex-item">
              <label htmlFor="username">Username:</label>
              <input 
              type="text" 
              id="username" 
              name="username" 
              className="form-input" 
              required />
            </div>

            <div className="flex-item">
              <label htmlFor="password">Password:</label>
              <input 
              type="password" 
              id="password" 
              name="password" 
              className="form-input" 
              required />
            </div>

            <div className="flex-item">
              <label htmlFor="password-again">Password (again):</label>
              <input 
              type="password" 
              id="password-again" 
              name="password-again" 
              className="form-input" 
              required />
            </div>

            <div className="flex-item">
              <label htmlFor="email">Email:</label>
              <input 
              type="email" 
              id="email" 
              name="email" 
              className="form-input" 
              required />
            </div>
            <br/>
            <div className="flex-item button-container">
              <button type="button" className="form-button" onClick={onSubmit}>
              Submit
              </button>
            </div>  
          </form>
        </div>
      </div>
    </div>
  );
}

export default CreateAccount