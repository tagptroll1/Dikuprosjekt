export async function get(req, res) {
  if (req.session && req.session.apiKey) {
    return res.end("yes")
  }
  return res.end("no")

}