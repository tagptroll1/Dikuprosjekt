export async function runCode(data) {
  try {
    const resp = await fetch(`${process.env.API_URL}/api/v1/coderunner`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });
    return await resp.json();
  } catch (err) {
    console.log(`Data post failed ${err}`);
  }
}
