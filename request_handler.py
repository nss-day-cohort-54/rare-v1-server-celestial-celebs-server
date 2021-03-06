from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from views import get_single_post, get_all_posts, get_all_tags, get_single_tag, get_all_categories, create_category, get_single_category
from views.coments_requests import get_all_post_comments
from views.post_request import get_all_user_posts, create_post, get_posts_by_category, edit_post, delete_post
from views.tags_requests import create_tag, get_all_postTags
from views.user import create_user, login_user
from views.user_requests import get_all_users, get_single_user
from views.subscription_requests import get_all_subscriptions, get_single_subscription, create_subscription


class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self):
        """Parse the url into the resource and id"""
        path_params = self.path.split('/')
        resource = path_params[1]
        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """Handle Get requests to the server"""
        self._set_headers(200)
        response = {}
        parsed = self.parse_url()

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/posts` or `/posts/2`
        if len(parsed) == 2:
            (resource, id) = parsed

            if resource == "posts":
                if id is not None:
                    response = f"{get_single_post(id)}"
                else:
                    response = f"{get_all_posts()}"
            if resource == "categories":
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = f"{get_all_categories()}"
            if resource == "posts":
                if id is not None:
                    response = f"{get_single_post(id)}"
                else:
                    response = f"{get_all_posts()}"
            if resource == "tags":
                if id is not None:
                    response = f'{get_single_tag(id)}'
                else:
                    response = f'{get_all_tags()}'
            if resource == "posttags":
                response = f'{get_all_postTags()}'
            if resource == "users":
                if id is not None:
                    response = f'{get_single_user(id)}'
                else:
                    response = f'{get_all_users()}'
                    
            if resource == "subscriptions":
                if id is not None:
                    response = f'{get_single_subscription(id)}'
                else:
                    response = f'{get_all_subscriptions()}'

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/post?user_id=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed


            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?

            # if key == "q" and resource == "categories":
            #     response = search_entries(value)
            if key == "user_id" and resource == "users":
                response = get_all_user_posts(value)
            if key == "user_id" and resource == "posts":
                response = get_all_user_posts(value)
            if key == "category_id" and resource == "posts":
                response = get_posts_by_category(value)
            if key == "post_id" and resource == "comments":
                response = get_all_post_comments(value)

        self.wfile.write(response.encode())


    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = ''
        resource, _ = self.parse_url()

        if resource == 'login':
            response = login_user(post_body)
        if resource == 'register':
            response = create_user(post_body)
        if resource == 'categories':
            response = create_category(post_body)
        if resource == 'posts':
            response = create_post(post_body)
        if resource == 'tags':
            response = create_tag(post_body)
        if resource == 'subscriptions':
            response = create_subscription(post_body)

        self.wfile.write(response.encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url()

        success = False

        if resource == "posts":
            success = edit_post(id, post_body)


        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url()

        # Delete a single post from the list
        if resource == "posts":
            delete_post(id)

    # Encode the new entry and send in response
        self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
