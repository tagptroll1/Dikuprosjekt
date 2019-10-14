export async function get(req, res) {
  console.log(!!req.session.apiKey)
}