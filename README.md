## Basic Python Discord LLM Chatbot

Basic Discord chatbot using [Discord Pi](https://github.com/Rapptz/discord.py) and [LangChain](https://github.com/langchain-ai/langchain). The bot is designed to interact with Discord channel users in a conversational manner, leveraging language models (LLM), and conversational memory to provide engaging responses.

## Installation

### 1. Initialize a new Git repository on your local machine
```
bash git init <repo>
cd <repo>
```

### 2. Add this repository to the specific folder:
```
git remote add -f origin https://github.com/shaunbarnard/python.git
```

### 3. Enable the sparse-checkout feature and specify the folder (llm-discord-chatbot) you want to clone:
```
git sparse-checkout init --cone
git sparse-checkout set llm-discord-chatbot
```

### 4. Finally, check out the contents of the specified folder (llm-discord-chatbot)
```
git checkout @
```

This approach allows you to work with only the contents of the specified folder ([llm-discord-chatbot])(https://github.com/langchain-ai/langchain), rather than cloning my entire Python repository and then removing unwanted files and folders.

```py
from tinygrad import Tensor, nn

class LinearNet:
  def __init__(self):
    self.l1 = Tensor.kaiming_uniform(784, 128)
    self.l2 = Tensor.kaiming_uniform(128, 10)
  def __call__(self, x:Tensor) -> Tensor:
    return x.flatten(1).dot(self.l1).relu().dot(self.l2)

model = LinearNet()
optim = nn.optim.Adam([model.l1, model.l2], lr=0.001)

x, y = Tensor.rand(4, 1, 28, 28), Tensor([2,4,3,7])  # replace with real mnist dataloader

for i in range(10):
  optim.zero_grad()
  loss = model(x).sparse_categorical_crossentropy(y).backward()
  optim.step()
  print(i, loss.item())
```

See [examples/beautiful_mnist.py](examples/beautiful_mnist.py) for the full version that gets 98% in ~5 seconds

## Accelerators

tinygrad already supports numerous accelerators, including:

- [x] [CPU](tinygrad/runtime/ops_cpu.py)
- [x] [GPU (OpenCL)](tinygrad/runtime/ops_gpu.py)
- [x] [C Code (Clang)](tinygrad/runtime/ops_clang.py)
- [x] [LLVM](tinygrad/runtime/ops_llvm.py)
- [x] [METAL](tinygrad/runtime/ops_metal.py)
- [x] [CUDA](tinygrad/runtime/ops_cuda.py)
- [x] [Triton](extra/triton/triton.py)
- [x] [PyTorch](tinygrad/runtime/ops_torch.py)
- [x] [HIP](tinygrad/runtime/ops_hip.py)
- [x] [WebGPU](tinygrad/runtime/ops_webgpu.py)

And it is easy to add more! Your accelerator of choice only needs to support a total of ~25 low level ops.
More information can be found in the [documentation for adding new accelerators](/docs/adding_new_accelerators.md).

## Installation

The current recommended way to install tinygrad is from source.

### From source

```sh
git clone https://github.com/tinygrad/tinygrad.git
cd tinygrad
python3 -m pip install -e .
```

### Direct (master)

```sh
python3 -m pip install git+https://github.com/tinygrad/tinygrad.git
```

## Documentation

Documentation along with a quick start guide can be found in the [docs/](/docs) directory.

### Quick example comparing to PyTorch

```py
from tinygrad import Tensor

x = Tensor.eye(3, requires_grad=True)
y = Tensor([[2.0,0,-2.0]], requires_grad=True)
z = y.matmul(x).sum()
z.backward()

print(x.grad.numpy())  # dz/dx
print(y.grad.numpy())  # dz/dy
```

The same thing but in PyTorch:
```py
import torch

x = torch.eye(3, requires_grad=True)
y = torch.tensor([[2.0,0,-2.0]], requires_grad=True)
z = y.matmul(x).sum()
z.backward()

print(x.grad.numpy())  # dz/dx
print(y.grad.numpy())  # dz/dy
```

## Contributing

There has been a lot of interest in tinygrad lately. Following these guidelines will help your PR get accepted.

We'll start with what will get your PR closed with a pointer to this section:

- No code golf! While low line count is a guiding light of this project, anything that remotely looks like code golf will be closed. The true goal is reducing complexity and increasing readability, and deleting `\n`s does nothing to help with that.
- All docs and whitespace changes will be closed unless you are a well-known contributor. The people writing the docs should be those who know the codebase the absolute best. People who have not demonstrated that shouldn't be messing with docs. Whitespace changes are both useless *and* carry a risk of introducing bugs.
- Anything you claim is a "speedup" must be benchmarked. In general, the goal is simplicity, so even if your PR makes things marginally faster, you have to consider the tradeoff with maintainablity and readablity.
- In general, the code outside the core `tinygrad/` folder is not well tested, so unless the current code there is broken, you shouldn't be changing it.

Now, what we want:

- Bug fixes (with a regression test) are great! This library isn't 1.0 yet, so if you stumble upon a bug, fix it, write a test, and submit a PR, this is valuable work.
- Solving bounties! tinygrad [offers cash bounties](https://docs.google.com/spreadsheets/d/1WKHbT-7KOgjEawq5h5Ic1qUWzpfAzuD_J06N1JwOCGs/edit?usp=sharing) for certain improvements to the library. All new code should be high quality and well tested.
- Features. However, if you are adding a feature, consider the line tradeoff. If it's 3 lines, there's less of a bar of usefulness it has to meet over something that's 30 or 300 lines. All features must have regression tests. In general with no other constraints, your feature's API should match torch or numpy.
- Refactors that are clear wins. In general, if your refactor isn't a clear win it will be closed. But some refactors are amazing! Think about readability in a deep core sense. A whitespace change or moving a few functions around is useless, but if you realize that two 100 line functions can actually use the same 110 line function with arguments while also improving readability, this is a big win.
- Tests/fuzzers. If you can add tests that are non brittle, they are welcome. We have some fuzzers in here too, and there's a plethora of bugs that can be found with them and by improving them. Finding bugs, even writing broken tests (that should pass) with `@unittest.expectedFailure` is great. This is how we make progress.
- Dead code removal from core `tinygrad/` folder. We don't care about the code in extra, but removing dead code from the core library is great. Less for new people to read and be confused by.

### Running tests

You should install the pre-commit hooks with `pre-commit install`. This will run the linter, mypy, and a subset of the tests on every commit.

For more examples on how to run the full test suite please refer to the [CI workflow](.github/workflows/test.yml).

Some examples of running tests locally:
```sh
python3 -m pip install -e '.[testing]'  # install extra deps for testing
python3 test/test_ops.py                # just the ops tests
python3 -m pytest test/                 # whole test suite
```