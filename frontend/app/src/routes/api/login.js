import {compare} from "bcrypt";

export async function post(req, res) {
  let auth = req.header("Authorization");
  let [username, password] = auth.split(":");
  
  if (username !== process.env.username) {
    return res.status(401).end("Wrong username or password");
  }

  compare(password, process.env.password, (err, passRes) => {
    if (err) {
      res.status(500).end(err);
    }
    else if (passRes) {
      req.session.apiKey = process.env.API_KEY;
      res.end("Ok") 
    } 
    else {
      res.status(401).end("Wrong username or password");
    }
  })
}
