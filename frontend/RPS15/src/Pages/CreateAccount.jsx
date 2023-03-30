import './CreateAccount.css'

const CreateAccount = () => {
  return (
    <div>
      <link rel="stylesheet" href="CreateAccount.css" />
      <div className="login-container">
        <div className="flex-container" />
        <div className="flex-item">
          <p className="logo">Account Create</p>
        </div>
        <form className="create-account-form">
          <div className="flex-item">
            <label htmlFor="username">Username:</label>
            <input type="text" id="username" name="username" className="form-input" required />
          </div>
          <div className="flex-item">
            <label htmlFor="password">Password:</label>
            <input type="password" id="password" name="password" className="form-input" required />
          </div>
          <div className="flex-item">
            <label htmlFor="password-again">Password (again):</label>
            <input type="password" id="password-again" name="password-again" className="form-input" required />
          </div>
          <div className="flex-item">
            <label htmlFor="email">Email:</label>
            <input type="email" id="email" name="email" className="form-input" required />
          </div>
          <div className="flex-item">
            <button type="submit" className="form-button">Submit</button>
          </div>  
        </form>
      </div>
    </div>
  );
}

export default CreateAccount