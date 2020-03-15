import fetch from "node-fetch";


export async function post(req, res) {
  const { body } = req;

  try {
    const resp = await fetch(new URL("http://127.0.0.1:5000/api/v1/coderunner"), {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    });

    const json = await resp.json();
    res.json(json);
  } catch (err) {
    console.log(`Data post failed ${err}`);
  }
}
