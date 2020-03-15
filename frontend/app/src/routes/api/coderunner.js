import fetch from "node-fetch";


export async function post(req, res) {
  const { body } = req;

  try {
    const resp = await fetch(`${process.env.API_URL}/api/v1/data`, {
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
