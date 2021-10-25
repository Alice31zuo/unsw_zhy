const getJSON = (path, options) => fetch(path, options)
  .then((data) => {
    if (data.status === 200) {
      return data.json()
    } else {
      // data.json().then((message) => alert(message.error));
      data.json().then((message) => Promise.reject(message.error));
    }
  })

const backendURL = 'http://localhost:5005/';

export default class API {
  constructor (url = backendURL) {
    this.url = url;
  }

  post (path, options) {
    return getJSON(`${this.url}/${path}`, {
      ...options,
      method: 'POST',
    });
  }

  put (path, options) {
    return getJSON(`${this.url}/${path}`, {
      ...options,
      method: 'PUT',
    });
  }

  get (path, options) {
    return getJSON(`${this.url}/${path}`, {
      ...options,
      method: 'GET',
    });
  }

  delete (path, options) {
    return getJSON(`${this.url}/${path}`, {
      ...options,
      method: 'DELETE',
    });
  }
}
