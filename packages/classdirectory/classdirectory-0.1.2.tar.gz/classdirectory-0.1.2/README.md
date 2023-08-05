# classdirectory

Get your objects here.

## Usage

```python
from classdirectory import ClassDirectory
import your_module


cd = ClassDirectory(your_module)
matching_classes = cd.find(parent=your_module.Parent, regex='Something$')
```
