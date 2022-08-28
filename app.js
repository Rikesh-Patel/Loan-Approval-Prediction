export default async function handler(req, res) {
    if (req.method === 'POST') {
      res.redirect(302, '/predict.html')
    }
  }