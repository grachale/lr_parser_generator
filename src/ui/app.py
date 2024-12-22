from dash import Dash
from .layout import create_layout
from .callbacks import register_callbacks

# Initialize the Dash application
app = Dash(__name__)

# Set the application layout
app.layout = create_layout()

# Register all callbacks for the application
register_callbacks(app)

# Expose the underlying WSGI server for deployment
server = app.server
