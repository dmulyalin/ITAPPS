from flask import jsonify, g, request
from app import db
from app.api import api
from app.api.auth import basic_auth

@api.route('/api/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    expires_in = request.args.get('expires_in', None)
    if expires_in:
        token = g.current_user.get_token(expires_in=int(expires_in))
    else:
        token = g.current_user.get_token()
    db.session.commit()
    return jsonify({
        'token': token,
        'expires_at': g.current_user.api_token_expiration
    })

@api.route('/api/tokens/revoke', methods=['POST'])
@basic_auth.login_required
def revoke_user_token():
    g.current_user.revoke_token()
    db.session.commit()
    return jsonify({
        'Message': "Toke for user '{}' set to expire in 1 second".format(g.current_user.username)
    })