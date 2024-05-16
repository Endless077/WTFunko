import {useState, useEffect} from "react";

export const Products = () => {

    const [data, setData] = useState([])
    const [filter, setFilter] = useState(data)
    const [loading, setLoading] = useState(false)
    let componentMounted = true

    useEffect(() => {
        const getProducts = async () => {
            setLoading(true)
            const response = await fetch("https://fakestoreapi.com/products");
            if (componentMounted) {
                setData(await response.clone().json());
                setFilter(await response.json());
                setLoading(false)
                console.log(filter)
            }

            return () => {
                // eslint-disable-next-line react-hooks/exhaustive-deps
                componentMounted = false;
            }
        }

        getProducts();
    }, []);

    const Loading = () => {
        return (
            <>
                Loading...
            </>
        )
    }

    const filterProducts = (cat) => {
        const updateList = data.filter((x)=> x.category === cat);
        setFilter(updateList)
    }

    const ShowProducts = () => {
        return (
            <>
            <div className="buttons d-flex justify-content-center mb-5 pb-5">
                    <button className="btn btn-outline-dark me-2" onClick={()=>setFilter(data)}>All</button>
                    {/* eslint-disable-next-line react/no-unescaped-entities */}
                    <button className="btn btn-outline-dark me-2" onClick={()=>filterProducts("men's clothing")}>Men's Clothing</button>
                    {/* eslint-disable-next-line react/no-unescaped-entities */}
                    <button className="btn btn-outline-dark me-2" onClick={()=>filterProducts("women's clothing")}>Women's Clothing</button>
                    <button className="btn btn-outline-dark me-2" onClick={()=>filterProducts("jewelery")}>Jewelery</button>
                    <button className="btn btn-outline-dark me-2" onClick={()=>filterProducts("electronics")}>Electronic</button>
                </div>

                {filter.map((product) => {
                    // console.log(product, 'product')
                    const { id, title, price, image } = product
                    return (
                        <div key={id} className="col-md-3 mb-4 me-4">
                            <div className="card h-100 text-center p-4" style={{width: "18rem"}}>
                                <img src={image} className="card-img-top" alt={title} height={250}/>
                                <div className="card-body">
                                    <h5 className="card-title mb-0">{title.substring(0,12)}</h5>
                                    <p className="card-text lead fw-bold">${price}</p>
                                    <a href="#" className="btn btn-outline-dark">Buy now</a>
                                </div>
                            </div>
                        </div>
                    )
                })}
            </>
        )
    }

    return (
        <div>
            <div className="container my-5 py-5">
                <div className="row">
                    <div className="col-12 mb-5">
                        <h1 className="display-6 fw-bolder
                        text-center">Latest Products</h1>
                        <hr />
                    </div>
                </div>
                <div className="row justify-content-center">
                    {loading ? <Loading/> : <ShowProducts/>}
                </div>
            </div>
        </div>
    )
}
