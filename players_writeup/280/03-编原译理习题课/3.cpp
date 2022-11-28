//https://gcc.gnu.org/bugzilla/show_bug.cgi?id=54080
template <class T>
class vector
{
};

template <template <typename U> class Container,
	 typename Func
	 >
vector<int> foo(const Container<int>& input, const Func &func)
{
}

template <template <typename U> class OutType,
	 typename Func1,
	 typename FuncRest
	 >
auto foo(const vector<int> &input, const Func1 &func1, const FuncRest funcrest) -> decltype(foo<vector>(foo(input, func1), funcrest))
{
	return;
}

int main()
{
	vector<int> v1;
	foo<vector>(v1, 1, 1);
}

//flag{Sorry-to-infOrm-you-thaT-gnu-is-not-unIx}
