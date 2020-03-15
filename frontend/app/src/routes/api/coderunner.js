import fetch from "node-fetch";


export async function post(req, res) {
  const { body } = req;s
  const url = new URL(`${process.env.API_URL}/api/v1/coderunner`);
  
  try {
    const resp = await fetch(url, {
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
