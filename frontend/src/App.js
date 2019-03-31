import React, { Component } from 'react'
import './App.css'
import axios from 'axios'
import https from 'https'

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {file: '',imagePreviewUrl: ''}
  }

  _handleSubmit(e) {
    e.preventDefault();
    let file = this.state.imagePreviewUrl;
    const formData = new FormData();

    formData.append("file", file);
    const agent = new https.Agent({
      rejectUnauthorized: false
    });
    axios({method: 'post', url: "http://localhost:5000/upload", httpsAgent: agent, data: formData } )
      .then(res => console.log(res))
      .catch(err => console.warn(err));
  }

  uploadFile(e) {
  e.preventDefault();
  let file = this.state.fileToBeSent;
  const formData = new FormData();

  formData.append("file", file);

  axios
    .post("/api/upload", formData)
    .then(res => console.log(res))
    .catch(err => console.warn(err));
}

  _handleImageChange(e) {
    e.preventDefault();
    console.log('handle imageChange-', e.target.files[0]);
    let reader = new FileReader()
    let file = e.target.files[0]

    reader.onloadend = () => {
      this.setState({
        file: file,
        imagePreviewUrl: reader.result
      })
    }
    reader.readAsDataURL(file)
    }

  render() {
    let {imagePreviewUrl} = this.state;
    let $imagePreview = null
    if (imagePreviewUrl) {
      $imagePreview = (<img src={imagePreviewUrl} alt="" />)
    } else {
      $imagePreview = (<div className="previewText">Please select an Image for Preview</div>)
    }

    return (
      <div className="App">
        <div className="previewComponent">
          <form onSubmit={(e)=>this._handleSubmit(e)}>
            <input className="fileInput"
              type="file"
              onChange={(e)=>this._handleImageChange(e)} />
            <button className="submitButton"
              type="submit"
              onClick={(e)=>this._handleSubmit(e)}>Upload Image</button>
          </form>
          <div className="imgPreview">
            {$imagePreview}
          </div>
        </div>
      </div>
    )
  }
}

export default App
