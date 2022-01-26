import React, {useEffect, useState} from 'react'
import { loadPosts } from '../lookup'

  export function PostsList(props){
    const [posts, setPosts] = useState([{content: "123"}])
    
    useEffect(()=>{
      const myCallback = (response, status)=>{
        if(status === 200){
          setPosts(response)
        } else{
          alert("There was an error")
        }
      }
      loadPosts(myCallback)
  
    }, [])
    return posts.map((item, index)=>{
      return <Post post={item} key={`${index}-${item.id}`} className='my-5 py-5 border bg-white text-dark'/>
    })
  }

export function ActionBtn(props){
    const {post, action} = props
    const className = props.className ? props.className : 'btn btn-primary btn-sm'
    return action.type === 'like'?<button className={className}>{post.likes} Likes</button> : null
  }
  
 export function Post(props){
    const {post} = props
    const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
    return <div className={className}>
      <p>{post.id} - {post.content}</p>
      <div className='btn btn-group'>
        <ActionBtn post = {post} action = {{type: "like"}}/>
        <ActionBtn post = {post} action = {{type: "unlike"}}/>
      </div>
    </div>
  }
  